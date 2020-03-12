from __future__ import (
    division,
    absolute_import,
    with_statement,
    print_function,
    unicode_literals,
)
import torch.optim as optim
import torch.optim.lr_scheduler as lr_sched
import torch.nn as nn
from torch.utils.data import DataLoader
import etw_pytorch_utils as pt_utils
import pprint
import os.path as osp
import os
import argparse
import tqdm
import torch
import numpy as np

from pointnet2.models import Pointnet2SemMSG as Pointnet
from pointnet2.models.pointnet2_msg_sem import model_fn_decorator
from pointnet2.data import Indoor3DSemSeg

def evaluation(d_loader,file):
    preds=np.zeros((len(d_loader),args.num_points),dtype=np.int32)
    labels=np.zeros_like(preds)#ground_truth
    loss=np.zeros((len(d_loader),1))
    idx=np.zeros_like(loss)

    trainer.model.eval()
    total_loss = 0.0
    if not os.path.exists(file+"_meshes"):
        os.mkdir(file+"_meshes")

    for i, data in tqdm.tqdm(
        enumerate(d_loader, 0), total=len(d_loader), leave=False, desc="val"
    ):
        trainer.optimizer.zero_grad()

        pred, _, eval_res = trainer.model_fn(trainer.model, data, eval=True)
        total_loss += eval_res['loss']
        loss[i]=eval_res['loss']

        total_loss/=len(d_loader)
        _, classes = torch.max(pred, -1)#convert predictions to classes
        preds[i]=classes.cpu().numpy()
        labels[i]=data[1].cpu().numpy()
        idx[i]=data[-1].item()

        np.savetxt(file+"_meshes/"+str(i)+".txt",np.c_[np.squeeze(data[0][...,:3].cpu().numpy()),labels[i],preds[i]],delimiter=" ")

    np.savetxt(file+"_predictions.txt",preds,delimiter=" ")
    np.savetxt(file+"_labels.txt",labels,delimiter=" ")
    np.savetxt(file+"_loss.txt",loss,delimiter=" ")
    np.savetxt(file+"_test_idxs.txt",idx,delimiter=" ")


parser = argparse.ArgumentParser(description="Arg parser")
parser.add_argument(
    "-batch_size", type=int, default=32, help="Batch size [default: 32]"
)
parser.add_argument(
    "-num_points",
    type=int,
    default=30000,
    help="Number of points to train with [default: 4096]",
)
parser.add_argument(
    "-weight_decay",
    type=float,
    default=0,
    help="L2 regularization coeff [default: 0.0]",
)
parser.add_argument(
    "-lr", type=float, default=1e-2, help="Initial learning rate [default: 1e-2]"
)
parser.add_argument(
    "-lr_decay",
    type=float,
    default=0.5,
    help="Learning rate decay gamma [default: 0.5]",
)
parser.add_argument(
    "-decay_step",
    type=float,
    default=2e5,
    help="Learning rate decay step [default: 20]",
)
parser.add_argument(
    "-bn_momentum",
    type=float,
    default=0.9,
    help="Initial batch norm momentum [default: 0.9]",
)
parser.add_argument(
    "-bn_decay",
    type=float,
    default=0.5,
    help="Batch norm momentum decay gamma [default: 0.5]",
)
parser.add_argument(
    "-checkpoint", type=str, default=None, help="Checkpoint to start from"
)
parser.add_argument(
    "-epochs", type=int, default=100, help="Number of epochs to train for"
)
parser.add_argument(
    "-run_name",
    type=int,
    choices=[0,1],
    default=0,
    help="Use tensorboard_logger or not. Default: 0(False)",
)
parser.add_argument("--visdom-port", type=int, default=8097)
parser.add_argument("--visdom", action="store_true")
parser.add_argument("--colours",type=int,choices=[0,1],default=0,help="Use colour infromation or not. Default: 0(False)")
parser.add_argument("--output",required=True,help="Name and path to save the model's predictions, loss and ground truth.")
parser.add_argument("--weights",default="",help="File that contains the weight for each label")

lr_clip = 1e-5
bnm_clip = 1e-2

if __name__ == "__main__":
    args = parser.parse_args()

    if not os.path.exists(os.path.dirname(args.output)):
        print("Output path doesn't exist. Exiting...")
        exit()
    else:
        args.output+=("_"+str(args.epochs))
        print(args.output)
    log_name=None
    if args.run_name:
        log_name="./runs/"+args.output
    val_set = Indoor3DSemSeg(args.num_points,use_colour=args.colours,split="val")
    val_loader = DataLoader(
        val_set,
        batch_size=args.batch_size,
        pin_memory=True,
        num_workers=2,
        shuffle=True,
    )

    train_set = Indoor3DSemSeg(args.num_points,use_colour=args.colours,split="train")
    train_loader = DataLoader(
        train_set,
        batch_size=args.batch_size,
        pin_memory=True,
        num_workers=2,
        shuffle=True,
    )
    if args.colours:
        model = Pointnet(num_classes=27, input_channels=7, use_xyz=True)
    else:
        model = Pointnet(num_classes=27, input_channels=3, use_xyz=True)
    model.cuda()
    optimizer = optim.Adam(
        model.parameters(), lr=args.lr, weight_decay=args.weight_decay
    )

    lr_lbmd = lambda it: max(
        args.lr_decay ** (int(it * args.batch_size / args.decay_step)),
        lr_clip / args.lr,
    )
    bnm_lmbd = lambda it: max(
        args.bn_momentum
        * args.bn_decay ** (int(it * args.batch_size / args.decay_step)),
        bnm_clip,
    )

    # default value
    it = -1  # for the initialize value of `LambdaLR` and `BNMomentumScheduler`
    best_loss = 1e10
    start_epoch = 1

    # load status from checkpoint
    if args.checkpoint is not None:
        checkpoint_status = pt_utils.load_checkpoint(
            model, optimizer, filename=args.checkpoint.split(".")[0]
        )
        if checkpoint_status is not None:
            it, start_epoch, best_loss = checkpoint_status

    lr_scheduler = lr_sched.LambdaLR(optimizer, lr_lambda=lr_lbmd, last_epoch=it)
    bnm_scheduler = pt_utils.BNMomentumScheduler(
        model, bn_lambda=bnm_lmbd, last_epoch=it
    )

    it = max(it, 0)  # for the initialize value of `trainer.train`
    if args.weights!="":
        weights=torch.from_numpy(np.loadtxt(args.weights)).float().cuda()
        model_fn = model_fn_decorator(nn.CrossEntropyLoss(weight=weights))
    else:
        model_fn = model_fn_decorator(nn.CrossEntropyLoss(ignore_index=26))

    if args.visdom:
        viz = pt_utils.VisdomViz(port=args.visdom_port)
    else:
        viz = pt_utils.CmdLineViz()

    viz.text(pprint.pformat(vars(args)))

    if not osp.isdir("checkpoints"):
        os.makedirs("checkpoints")

    trainer = pt_utils.Trainer(
        model,
        model_fn,
        optimizer,
        checkpoint_name="checkpoints/"+os.path.basename(args.output),
        best_name="checkpoints/"+os.path.basename(args.output)+"_best",
        lr_scheduler=lr_scheduler,
        bnm_scheduler=bnm_scheduler,
        tensorboard_logger=log_name,
        viz=viz,
    )

    trainer.train(
        it, start_epoch, args.epochs, train_loader, val_loader, best_loss=best_loss
    )

    test_set = Indoor3DSemSeg(args.num_points,use_colour=args.colours, split="test")
    test_loader = DataLoader(
        test_set,
        batch_size=1,
        shuffle=True,
        pin_memory=False,
        num_workers=2,
    )
    evaluation(test_loader,args.output)

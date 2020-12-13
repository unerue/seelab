class AverageMeter:
    """
    Computes and stores the average and current value
    """

    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
        
from torch.utils.tensorboard import SummaryWriter


class TensorBoardLogger(Callback):
    def __init__(self, log_dir=".logs/"):
        self.writer = SummaryWriter(log_dir=log_dir, flush_secs=30)

    def on_train_epoch_end(self, model):
        for metric in model.metrics["train"]:
            self.writer.add_scalar(
                f"train/{metric}", model.metrics["train"][metric], model.current_epoch
            )

    def on_valid_epoch_end(self, model):
        for metric in model.metrics["valid"]:
            self.writer.add_scalar(
                f"valid/{metric}", model.metrics["valid"][metric], model.current_epoch
            )
import psutil
import torch
from torch import nn, Tensor

try:
    from torch.cuda.amp import GradScaler, autocast
    use_amp = True
except:
    pass


class BaseTrainer:
    def __init__(self):
        raise NotImplementedError


class TorchTrainer:
    def __init__(self):
        """
        Args:
        Returns:

        """
        self.model
        self.optimizer
        self.scheduler
        self.train_loader
        self.valid_loader
        self.criterion
        raise NotImplementedError

    def _init_trainer(self):
        self.num_gpus = torch.cuda.device_count()

        if use_amp:
            self.scaler = GradScaler()
            self.autocast = autocast()

    def train_one_step(self):
        raise NotImplementedError

    def valid_oen_step(self):
        raise NotImplementedError

    def train_one_epoch(self):
        self.model.train()
        for inputs, targets in self.train_loader:
            if use_amp:
                with self.autocast():
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs, targets)
                    self.scaler.scale(loss).backward()
                    self.scaler.step(self.optimizer)
                    self.scaler.update()
            else:
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                loss.backward()
                self.optimizer.step()

            if self.scheduler is not None:
                self.scheduler.step()

        raise NotImplementedError

    def valid_one_epoch(self):
        raise NotImplementedError

    
    def update_log(self):
        return NotImplementedError




        
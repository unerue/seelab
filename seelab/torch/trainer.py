import psutil
from typing import Optional
import torch
import torch.optim as optim
from torch import nn, Tensor
from torch.utils.data import DataLoader
try:
    from torch.cuda.amp import GradScaler, autocast
    from torch.multiprocessing as mp
    import torch.distributed as dist
    from torch.nn.parallel import DistributedDataParallel
    use_amp = True
except:
    pass



def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '1030'

    dist.init_process_group('gloo', rank=rank, world_size=world_size)

def cleanup():
    dist.destroy_process_group()


def demo_basic(rank, world_size):
    setup(rank, world_size)

    model = None
    model.to(rank)
    ddp_model = DistributedDataParallel(model, device_ids=[rank])

    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=1e-3)


    cleanup()

def run_demo(demo_fn, world_size):
    mp.spawn(demo_fn, agrs=(world_size,), nprocs=world_size, join=True)



class BaseTrainer:
    def __init__(self):
        raise NotImplementedError





class TorchTrainer:
    def __init__(
        self, model: nn.Module, optimizer: optim, criterion: nn.Module, 
        train_loder: DataLoader, valid_loader: Optional[DataLoader] = None,
        scheduler: Optional[optim.lr_scheduler] = None):
        """Trainer for PyTorch
        Arguments:
            model (nn.Module)
            optimizer (torch.optim)
            criterion (nn.Module)
            train_loader (DataLoader)
            valid_loader (Optional[DataLoader])
            scheduler (Optional[torch.optim.lr_scheduler])
        Returns:
            
        """
        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion
        self.train_loader = train_loder
        self.valid_loader = valid_loader
        self.scheduler = scheduler
        self.config_train = config_train
        self._init_trainer()

    def _init_trainer(self):
        self.num_gpus = torch.cuda.device_count()
        factor = self.config_train.get('batch_size') / 8
        self.config_train['lr']
        self.config_train['max_iter'] //= factor
        if use_amp:
            self.scaler = GradScaler()

        if self.num_gpus > 1:
            self.

    
    def custom_parallel(self):
        from torch.nn.parallel import DistributedDataParallel



    def train_one_step(self, inputs, targets):
        if use_amp:
            with autocast():
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

        return outputs

    @torch.no_grad()
    def valid_one_step(self, inputs, targets):
        return NotImplementedError

    def train_one_epoch(self, inputs, targets):
        self.train_one_step(inputs, targets)

    def valid_one_epoch(self, inputs, targets):
        return NotImplementedError

    def train(self):
        self.model.train()
        for inputs, targets in self.train_loader:
            self.train_one_epoch(inputs, targets)

        self.model.eval()
        if self.valid_loader is not None:
            for inputs, targets in self.valid_loader:
                self.valid_one_epoch(inputs, targets)

    def update_log(self):
        return NotImplementedError




        
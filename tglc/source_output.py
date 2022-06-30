import os

os.environ["OPENBLAS_NUM_THREADS"] = "8"
os.environ["MKL_NUM_THREADS"] = "8"
os.environ["NUMEXPR_NUM_THREADS"] = "8"
os.environ["OMP_NUM_THREADS"] = "8"
from tglc.ffi import *
from multiprocessing import Pool
from functools import partial
import logging

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

def cut_ffi_(i, sector=1, size=150, local_directory=''):
    ffi(camera=1 + i // 4, ccd=1 + i % 4, sector=sector, size=size, local_directory=local_directory)


def ffi_to_source(sector=1, local_directory=''):
    """
    Cut calibrated FFI to source.pkl
    :param sector: int, required
    TESS sector number
    :param local_directory: string, required
    output directory
    """
    os.makedirs(f'{local_directory}lc/', exist_ok=True)
    os.makedirs(f'{local_directory}epsf/', exist_ok=True)
    os.makedirs(f'{local_directory}ffi/', exist_ok=True)
    os.makedirs(f'{local_directory}source/', exist_ok=True)
    os.makedirs(f'{local_directory}log/', exist_ok=True)

    with Pool(4) as p:
        p.map(partial(cut_ffi_, sector=sector, size=150, local_directory=local_directory), range(16))

    # for i in range(16):
    #     ffi(camera=1 + i // 4, ccd=1 + i % 4, sector=sector, size=150, local_directory=local_directory)


if __name__ == '__main__':
    sector = 3
    ffi_to_source(sector=sector, local_directory=f'/home/tehan/data/sector{sector:04d}/')

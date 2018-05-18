from . import bioinf_utils
from .. import dataset_pb2
import edlib

def fillDataPoint(dp: dataset_pb2.DataPoint, cigar: str=None):
    """

    :param dp:
    :param basecalled:
    :param aligned_basecalled:
    :return:
    """
    if cigar is None:
        res = edlib.align(
            "".join([dataset_pb2.BasePair.Name(x) for x in dp.basecalled]),
            "".join([dataset_pb2.BasePair.Name(x) for x in dp.aligned_ref]),
        task="path")
        cigar = bioinf_utils.decompress_cigar(res['cigar'])

    ref_idx = 0
    bcall_idx = 0

    aligned_ref_squiggle = []
    basecalled_squiggle = []
    cigar_lst = []

    for cigar in cigar:
        if cigar in bioinf_utils.CIGAR_MATCH_MISSMATCH:
            cigar_lst.append(
                dataset_pb2.MATCH
                if cigar in bioinf_utils.CIGAR_MATCH else dataset_pb2.MISMATCH
            )
            aligned_ref_squiggle.append(dp.aligned_ref[ref_idx])
            basecalled_squiggle.append(dp.basecalled[bcall_idx])
            ref_idx += 1
            bcall_idx += 1
        elif cigar in bioinf_utils.CIGAR_INSERTION:
            cigar_lst.append(dataset_pb2.INSERTION)
            basecalled_squiggle.append(dp.basecalled[bcall_idx])
            aligned_ref_squiggle.append(dataset_pb2.BLANK)
            bcall_idx += 1
        elif cigar in bioinf_utils.CIGAR_DELETION:
            cigar_lst.append(dataset_pb2.DELETION)
            basecalled_squiggle.append(dataset_pb2.BLANK)
            aligned_ref_squiggle.append(dp.aligned_ref[ref_idx])
            ref_idx += 1
        else:
            raise ValueError(f"Not sure what to do with {cigar}")

    assert len(cigar_lst) == len(aligned_ref_squiggle)
    assert len(cigar_lst) == len(basecalled_squiggle)
    assert ref_idx == len(dp.aligned_ref)
    assert bcall_idx == len(dp.basecalled)

    dp.MergeFrom(
        dataset_pb2.DataPoint(
            cigar=cigar_lst,
            aligned_ref_squiggle=aligned_ref_squiggle,
            basecalled_squiggle=basecalled_squiggle,
        )
    )

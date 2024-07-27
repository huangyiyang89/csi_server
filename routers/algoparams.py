from fastapi import APIRouter, HTTPException,Depends
from sqlmodel import Session, select
from database import get_session
from models.algoparam import AlgoParam,AlgoParamPublic,AlgoParamCreate,AlgoParamUpdate

router = APIRouter(
    prefix="/algoparams",
    tags=["algoparams"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[AlgoParamPublic])
def get_algoparams(*, session: Session = Depends(get_session)):
    """
    获取所有算法参数

    返回:
        list[AlgoParamRead]: 所有算法参数的列表
    """
    return session.query(AlgoParam).all()


@router.get("/{algoparam_id}", response_model=AlgoParamPublic)
def get_algoparam(*, session: Session = Depends(get_session), algoparam_id: int):
    """
    根据ID获取算法参数

    参数:
        algoparam_id (int): 算法参数的ID

    返回:
        AlgoParamRead: 指定ID的算法参数，如果ID不存在则返回404
    """
    algoparam = session.get(AlgoParam, algoparam_id)
    if not algoparam:
        raise HTTPException(status_code=404, detail="AlgoParam not found")
    return algoparam


@router.post("/", response_model=AlgoParamPublic)
def create_algoparam(*, session: Session = Depends(get_session), algoparam: AlgoParamCreate):
    """
    创建新的算法参数

    参数:
        algoparam (AlgoParamCreate): 新算法参数的详细信息

    返回:
        AlgoParamRead: 新创建的算法参数
    """
    db_algoparam = AlgoParam.model_validate(algoparam)
    session.add(db_algoparam)
    session.commit()
    session.refresh(db_algoparam)
    return db_algoparam


@router.put("/{algoparam_id}", response_model=AlgoParamPublic)
def update_algoparam(*, session: Session = Depends(get_session), algoparam_id: int, algoparam: AlgoParamUpdate):
    """
    根据ID更新算法参数

    参数:
        algoparam_id (int): 要更新的算法参数的ID
        algoparam (AlgoParamUpdate): 新的算法参数详细信息

    返回:
        AlgoParamRead: 更新后的算法参数，如果ID不存在则返回404
    """
    db_algoparam = session.get(AlgoParam, algoparam_id)
    if not db_algoparam:
        raise HTTPException(status_code=404, detail="AlgoParam not found")

    for key, value in algoparam.model_dump().items():
        setattr(db_algoparam, key, value)

    session.commit()
    session.refresh(db_algoparam)
    return db_algoparam


@router.delete("/{algoparam_id}")
def delete_algoparam(*, session: Session = Depends(get_session), algoparam_id: int):
    """
    根据ID删除算法参数

    参数:
        algoparam_id (int): 要删除的算法参数的ID

    返回:
        dict: 删除操作的结果消息
    """
    db_algoparam = session.get(AlgoParam, algoparam_id)
    if not db_algoparam:
        raise HTTPException(status_code=404, detail="AlgoParam not found")

    session.delete(db_algoparam)
    session.commit()
    return {"message": "AlgoParam deleted"}

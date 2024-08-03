from fastapi import APIRouter, HTTPException,Depends
from sqlmodel import Session, select
from database import get_session
from models.algoparam import AlgoParam,AlgoParamUpdate



router = APIRouter(
    prefix="/api/algoparams",
    tags=["algoparams"]
)

@router.get("/")
def get_algoparam(*, session: Session = Depends(get_session)) -> list[AlgoParam]:

    algoparams = session.exec(select(AlgoParam)).all()
    if not algoparams:
        raise HTTPException(status_code=404)
    return algoparams


@router.get("/{algoparam_id}")
def get_algoparam(*, session: Session = Depends(get_session), algoparam_id: int)-> AlgoParam:
    algoparam = session.get(AlgoParam, algoparam_id)
    if not algoparam:
        raise HTTPException(status_code=404)
    return algoparam

@router.patch("/{algoparam_id}")
def patch_algoparam(*, session: Session = Depends(get_session), algoparam_id: int, algoparam: AlgoParamUpdate)-> AlgoParam:
    db_algoparam = session.get(AlgoParam, algoparam_id)
    if not db_algoparam:
        raise HTTPException(status_code=404)
    
    for key, value in algoparam.model_dump(exclude_unset=True).items():
        setattr(db_algoparam, key, value)
    
    session.commit()
    session.refresh(db_algoparam)
    return db_algoparam

@router.delete("/{algoparam_id}")
def delete_algoparam(*, session: Session = Depends(get_session), algoparam_id: int):
    db_algoparam = session.get(AlgoParam, algoparam_id)
    if not db_algoparam:
        raise HTTPException(status_code=404)
    session.delete(db_algoparam)
    session.commit()
    return None

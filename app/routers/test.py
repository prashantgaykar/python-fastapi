from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/force_update",tags=['test'])

class ForceUpdate():
    current_version: str
    min_version: str

@router.get("/")
def get_force_update():
    ios = ForceUpdate()
    ios.current_version = "1.1.1.1"
    ios.min_version = "1.1.1.1"

    android = ForceUpdate()
    android.current_version = "1.21.12.29"
    android.min_version = "1.21.12.29"

    android_hwi = ForceUpdate()
    android_hwi.current_version = "1.21.12.27"
    android_hwi.min_version = "1.21.12.27"

    update_data = dict()
    update_data.update({"ios":ios})
    update_data.update({"android":android})
    update_data.update({"android_hwi":android_hwi})
    return update_data
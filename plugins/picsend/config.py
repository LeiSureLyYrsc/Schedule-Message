from pydantic import BaseModel

class Config(BaseModel):
    pic_path: list[str] = ['./congyu/congyu.jpg']
    picsend_group: list[str] = ['123123']
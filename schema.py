import pydantic


class AdvertisementBase(pydantic.BaseModel):
    title: str
    description: str

    @pydantic.field_validator("description")
    @classmethod
    def check_description(cls, value):
        if len(value) < 8:
            raise ValueError("description is too short")
        return value


class CreateAdvertisement(AdvertisementBase):
    title: str
    description: str


from pydantic import BaseModel
class ReturnInfo(BaseModel):
    name: str
    city: str
    state: str
    employee_count : int
    linkedin : str
    website : str
    apollo : str
    industry: str
    revenue: str
    product_category: str
    type: list[str]
    year_founded: int
    person_first : str
    person_last : str
    title : str
    owner_li : str

instruction = """
You are a data extraction agent. You are given a company profile page from Apollo.io. Your task is to extract specific company information and return it as a JSON based on a provided schema.

The schema is as follows:
fit : if the company fits the criteria
why : short description why its a fit / not a fit
name: The company's name  
city: City of the company's headquarters  
state: State or region of the headquarters  
employee_count : number of employees
linkedin: LinkedIn company profile URL  
website : Company URL
apollo : Apollo URL starts with https://app.apollo.io/#/organizations/ then some id 
industry: Industry sector the company belongs to  
revenue: Estimated company revenue (e.g., "$1M–$10M")  
product_category: The primary category of the company's product or service  
type: "B2B" or "B2C", based on the company's business model  
year_founded: The year the company was founded  
person_first : person in charge first name (to contact ideally owner, founder, ceo) if they are all low ranking PUT N/A
person_last : person in charge last name (to contact ideally owner, founder, ceo) if they are all low ranking PUT N/A
title : persons in charge title
owner_li : owners/person in charge linkedin URL

Search Criteria:
"""
import graphene

from graphene_django import DjangoObjectType

from fohat.mycompanies.models import Company, Employee

class CompanyType(DjangoObjectType):
  class Meta:
    model = Company
    fields = ("id", "name", "cnpj")

class CreateCompany(graphene.Mutation):
    company = graphene.Field(CompanyType)

    class Arguments:
      name = graphene.String(required=True)
      cnpj = graphene.String(required=True)

    def mutate(self, info, name, cnpj):
      company = Company(
        name=name,
        cnpj=cnpj
      )
      company.save()

      return CreateCompany(company=company)

class UpdateCompany(graphene.Mutation):
    class Arguments:
      id = graphene.ID()
      name = graphene.String(required=True)
      cnpj = graphene.String(required=True)

    company = graphene.Field(CompanyType)

    def mutate(self, info, id, name, cnpj):
      company = Company.objects.get(pk=id)
      company.name = name
      company.cnpj = cnpj
      company.save()
      return UpdateCompany(company=company)

class DeleteCompany(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    def mutate(self, info, **kwargs):
        obj = Company.objects.get(pk=kwargs["id"])
        obj.delete()
        return DeleteCompany(ok=True)

class EmployeeType(DjangoObjectType):
  class Meta:
    model = Employee
    fields = ("id", "name", "cpf")

class CreateEmployee(graphene.Mutation):
    employee = graphene.Field(EmployeeType)
    
    class Arguments:
      name = graphene.String(required=True)
      cpf = graphene.String(required=True)

    def mutate(self, info, name, cpf):
      employee = Employee(
        name=name,
        cpf=cpf
      )
      employee.save()

      return CreateEmployee(employee=employee)

class UpdateEmployee(graphene.Mutation):
    class Arguments:
      id = graphene.ID()
      name = graphene.String(required=True)
      cpf = graphene.String(required=True)

    employee = graphene.Field(EmployeeType)

    def mutate(self, info, id, name, cpf):
      employee = Employee.objects.get(pk=id)
      employee.name = name
      employee.cpf = cpf
      employee.save()
      return UpdateEmployee(employee=employee)

class DeleteEmployee(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    def mutate(self, info, **kwargs):
        obj = Employee.objects.get(pk=kwargs["id"])
        obj.delete()
        return DeleteEmployee(ok=True)

class Query(graphene.ObjectType):
  company = graphene.Field(CompanyType, id=graphene.Int())
  all_companies = graphene.List(CompanyType)
  employee = graphene.Field(EmployeeType, id=graphene.Int())
  all_employees = graphene.List(EmployeeType)

  def resolve_company(self, info, **kwargs):
    id = kwargs.get("id")
    if id:
      return Company.objects.get(id=id)
  
  def resolve_all_companies(self, info, **kwargs):
    return Company.objects.all()

  def resolve_employee(self, info, **kwargs):
    id = kwargs.get("id")
    if id:
      return Employee.objects.get(id=id)
  
  def resolve_all_employees(self, info, **kwargs):
    return Employee.objects.all()

class Mutation(graphene.ObjectType):
    create_company = CreateCompany.Field()
    create_employee = CreateEmployee.Field()
    delete_company = DeleteCompany.Field()
    delete_employee = DeleteEmployee.Field()
    update_company = UpdateCompany.Field()
    update_employee = UpdateEmployee.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

#   BLL
import pymysql  # FOR CONNECTING MYSQL
from time import sleep

# CLASS FOR CUSTOMERS
class customer:
    # CONNECTION FROM DATABASE
    mycon = pymysql.connect(host="localhost", user="coding-paradise", password="99972965", database="vendingMACHINE")
    mycur = mycon.cursor()

    # CONSTRUCTOR
    def __init__(self):
        self.name=0
        self.id=0
        self.tea_type=0
        self.data=0
    #   FUNCTION FOR DISPLAY TEA OR COFFE TYPE
    def displayTEAorCOFFEtypes(self,ch):
        if ch==1:ch='tea'
        else:ch='coffee'
        qry="select * from %s"%ch
        customer.mycon.ping()
        customer.mycur.execute(qry)
        self.data=customer.mycur.fetchall()
        for i in range(len(self.data)):print(f"{i+1}:{self.data[i]}")

    # FUNCTION FOR ADDING SECOND CHOICE,LIKE IF ONE HAVE TEA CHOICE AND WANT COFFEE SOO IT WILL ADD COFFEE TYPE TOO
    def addSecondCHOICE(self,ch):
        if ch==1:ch='tea_type'
        else:ch= 'coffee_type'
        qry="update customer set %s=%a where name =%a"%(ch,self.tea_type,self.name)
        customer.mycur.execute(qry)
        customer.mycon.commit()
        customer.mycon.close()

    # FUCNTION FOR ADDING NEW CUSTOMER
    def addCUSTOMER(self,ch):
        if ch == 1: ch = 'tea_type'
        else:ch = 'coffee_type'
        qry="insert into customer(name,%s) values(%a,%a)"%(ch,self.name,self.tea_type)
        customer.mycur.execute(qry)
        customer.mycur.execute("SELECT @@IDENTITY")
        self.data=customer.mycur.fetchone()
        print(f"your unique id is ({self.data[0]}) sir.")
        customer.mycon.commit()
        customer.mycon.close()
    # FUNCTION FOR AUTHENTICATE CUSTOMER EXISTENCE
    def authCUSTOMER(self,ch):
        try:
            if ch==1:
                ch='TEA'
                qry=f"select tea_type from customer  where name =%a"%(self.name)
            if ch==2:
                ch='COFFEE'
                qry=f"select coffee_type from customer  where name =%a"%(self.name)
            customer.mycur.execute(qry)
            self.data = customer.mycur.fetchone()[0]
            customer.mycon.close()
            global t
            t=0
            if self.data == None:   # IT RUN WHEN CUSTOMER EXIST WITH TEA/COFFEE BUT WANT COFFEE/TEA
                t=1
                print(f"PLEASE SELECT WHICH TYPE OF {ch} YOU WANT TO PREFER SIR :-")
                return False
            else:
                self.tea_type = self.data[0]
                return True
        except: print(f"PLEASE SELECT WHICH TYPE OF {ch} YOU WANT TO PREFER SIR :-")    # WHEN CUSTOMER NOT EXIST

# MACHINE CLASS
class machine():
    mycon = pymysql.connect(host="localhost", user="coding-paradise", password="99972965", database="vendingMACHINE")
    mycur = mycon.cursor()

    # CONSTRUCTOR
    def __init__(self):
        self.m_id='MH100'
        self.capacity=30

    #   FUNCTION FOR DISPLAY MACHINE TABLE IN DATABASE
    def displayMATERIALwithQUNATITY(self):
        qry="select * from machine"
        supplier.mycur.execute(qry)
        return supplier.mycur.fetchall()

    #   FUNCTION FOR DISPLAY MATERIAL FROM MACHINE TABLE
    def displayMATERIAL(self):
        qry = "select material from machine"
        supplier.mycur.execute(qry)
        return supplier.mycur.fetchall()

    #   FUNCTION FOR PREPARING SELECTED/FAVORITE TEA/COFFEE
    def prepareTEAorCOFFEE(self):

        l = [f"PREPARING YOUR FAVORITE ONE.\n\t\t\tPLEASE WAIT ! ............", "YOUR ORDER IS READY SIR . PLEASE COLLECT IT."]
        for i in range(2):
            print(l[i]); sleep(5)

    # FUNCTION FOR CHECKING FOR OVER-CAPACITY OF MACHINE
    def acceptMATERIAL(self):
        quantity=supplier().quantity
        qry = "select sum(quantity_kg_or_lit) from machine"
        machine.mycur.execute(qry)
        total_quan = supplier.mycur.fetchone()[0]
        if total_quan + quantity > machine().capacity:
            return False
        else: return True

    # FOR MACHINE ON
    def machineON(self):
        print("HELLO SIR !")

    # FOR MACHINE OFF
    def machineOFF(self):
        print("GOOD BYE !")

#   CLASS FOR SUPPLIER
class supplier(machine):

    def __init__(self):
        self.s_id=10
        self.emp_type=0
        self.quantity=0

    # FUNCTION FOR SUPPLYING MATERIAL IN MACHINE
    def suppliMATERIAL(self,material):
        if supplier.acceptMATERIAL(self):
            qry="select quantity_kg_or_lit from machine where material=%a"%material
            supplier.mycur.execute(qry)
            int_=supplier.mycur.fetchone()[0]
            qry = "update machine set quantity_kg_or_lit = %a where material=%a"%(int_+self.quantity,material)
            supplier.mycur.execute(qry)
            supplier.mycon.commit()
            supplier.mycon.close()
        else:
            print("MACHINE IS ALREADY FULL SIR.")

    #   FUNCTION FOR CLEANING MACHINE
    def cleanMACHINE(self,m_id):
        if m_id==machine().m_id:
            s.machineOFF()
            return True
        else: False


# PL
if __name__=='__main__':
    try:
        cus=customer()
        s=supplier()
        status=False
        print("HELLO WELCOME SIR!")
        while(1):

            ch=input("PRESS //S FOR SUPPLIER MODE//, //C for customer//,//E for exit//:")

            # FOR SUPPLIER :-
            if ch=='s'or ch=='S':
                id=int(input("PLEASE INPUT supplier_ID:-"))
                if id==s.s_id:
                    ch=int(input("1. SUPPLY MATERIAL 2. CLEAN MACHINE 3. DISPLAY(MATERIAL_WITH_QUANTITY).:-\t"))
                    if ch==1:
                        data = s.displayMATERIAL()
                        for i in range(len(data)):
                            print(f"{i + 1}:{data[i]}", end='  ')
                        temp=data[int(input("\nSELECT ABOVE MATERIAL TO PUT IN:-\t"))-1][0]
                        s.quantity = int(input("ENTER QUANTITY(KG/LIT):-\t"))
                        s.suppliMATERIAL(temp)
                    if ch==2:
                        if s.cleanMACHINE(input("PLEASE ENTER MACHINE ID:\t")):
                            print("MACHINE STATUS:- OFF")
                            print("Go Ahed")
                            ch=input("PRESS 'S' FOR START THE MACHINE:- ")
                            if ch=='s' or ch=='S': 
                                s.machineON()
                        else:print("WRONG MACHINE ID :(")
                    if ch==3:
                        print(s.displayMATERIALwithQUNATITY())
                else:print("WRONG ID :(")


            # FOR CUSTOMER :-
            elif ch=='c'or ch=='C':
                cus.name = input("WHAT IS YOUR GOOD NAME SIR ? :-\t\t")
                ch=int(input("WHAT DO YOU LIKE TO HAVE SIR ? :-\n\t\t 1-TEA OR 2-COFFEE:\t"))
                #   for tea choice:

                status=cus.authCUSTOMER(ch)
                if status:
                    s.prepareTEAorCOFFEE()

                else:
                    cus.displayTEAorCOFFEtypes(ch)
                    cus.tea_type = str(cus.data[int(input("\n")) - 1][0])
                    if t==1:cus.addSecondCHOICE(ch)
                    else:cus.addCUSTOMER(ch)
                    s.prepareTEAorCOFFEE()


            #   FOR EXIT()
            elif ch=='E' or ch=='e':
                exit()
            else:print("WRONG CHOICE:(")
            print("\n")
    except Exception as e: print(f"\n{e}:(")






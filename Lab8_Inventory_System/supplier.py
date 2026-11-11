class Supplier:

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if "@" not in contact_email:
            raise ValueError("Contact email must contain '@'.")
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    # ---------- Getters (read-only access from outside) ----------

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    # ---------- Behaviour ----------

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
              f"Email: {self.__contact_email}")

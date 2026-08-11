from models import MenuItem, Order, OrderItem, create_customer


class CateringService:
    """Abstraction layer used by web routes; routes never write SQL."""

    def __init__(self, repository):
        self.repo = repository

    def add_customer(self, form):
        customer = create_customer(form["customer_type"], form["name"], form["phone"], form["address"])
        return self.repo.save_customer(customer)

    def add_menu(self, form):
        item = MenuItem(None, form["name"].strip(), form["category"], int(form["price"]), int(form["stock"]))
        self.repo.save_menu(item.name, item.category, item.price, item.stock)

    def create_order(self, form):
        row = self.repo.customer_by_id(int(form["customer_id"]))
        if not row:
            raise ValueError("Pelanggan tidak ditemukan.")
        customer = create_customer(row["customer_type"], row["name"], row["phone"], row["address"])
        menu_map = {m["id"]: m for m in self.repo.all_menus()}
        items = []
        for menu_id, menu in menu_map.items():
            quantity = int(form.get(f"qty_{menu_id}", 0) or 0)
            if quantity > menu["stock"]:
                raise ValueError(f"Stok {menu['name']} hanya {menu['stock']}.")
            if quantity > 0:
                items.append(OrderItem(menu_id, menu["name"], menu["price"], quantity))
        order = Order(customer, items, form["delivery_date"], form["payment_method"], form.get("notes", ""))
        return self.repo.save_order(row["id"], order)


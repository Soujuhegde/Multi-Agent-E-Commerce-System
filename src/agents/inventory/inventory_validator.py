class InventoryValidator:

    @staticmethod
    def validate_quantity(
        quantity: int
    ) -> bool:

        return quantity > 0
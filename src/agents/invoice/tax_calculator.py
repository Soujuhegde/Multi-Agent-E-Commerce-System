class TaxCalculator:

    GST = 18

    @staticmethod
    def calculate(
        amount: float
    ):

        return amount * (
            TaxCalculator.GST / 100
        )
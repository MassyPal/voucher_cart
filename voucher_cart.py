VOUCHER_VALUE = 8  # euro per buono pasto
MAX_VOUCHERS = 8  # massimo 8 buoni pasto (64 euro)


def calculate_payment(total: float) -> dict:
    """Calcola quanti buoni pasto interi usare e il resto da pagare in contanti.

    I buoni pasto vengono usati solo integralmente (8 euro ciascuno).
    Si usano al massimo 8 buoni (64 euro in totale).

    Args:
        total: importo totale della spesa in euro.

    Returns:
        Un dizionario con:
            - "vouchers": numero di buoni pasto usati
            - "voucher_amount": importo coperto dai buoni pasto (euro)
            - "cash": importo da pagare in contanti (euro)
    """
    if total < 0:
        raise ValueError("Il totale non può essere negativo")

    vouchers_usable = int(total // VOUCHER_VALUE)
    vouchers = min(vouchers_usable, MAX_VOUCHERS)
    voucher_amount = vouchers * VOUCHER_VALUE
    cash = round(total - voucher_amount, 2)

    return {
        "vouchers": vouchers,
        "voucher_amount": voucher_amount,
        "cash": cash,
    }

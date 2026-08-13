import pytest

from voucher_cart import calculate_payment


class TestCalculatePayment:
    """Test del calcolo dei buoni pasto (8 euro ciascuno, max 8 buoni = 64 euro)."""

    def test_total_below_one_voucher_uses_no_vouchers(self):
        """Spesa inferiore a 8 euro: nessun buono usato, si paga tutto in contanti."""
        result = calculate_payment(5.00)
        assert result["vouchers"] == 0
        assert result["voucher_amount"] == 0
        assert result["cash"] == 5.00

    def test_total_exactly_one_voucher(self):
        """Spesa esattamente uguale a 8 euro: 1 buono, 0 di contanti."""
        result = calculate_payment(8.00)
        assert result["vouchers"] == 1
        assert result["voucher_amount"] == 8
        assert result["cash"] == 0.00

    def test_total_between_vouchers_uses_floor(self):
        """Spesa di 15 euro: 1 buono (8 euro) + 7 euro di contanti."""
        result = calculate_payment(15.00)
        assert result["vouchers"] == 1
        assert result["voucher_amount"] == 8
        assert result["cash"] == 7.00

    def test_total_exactly_max_vouchers(self):
        """Spesa di 64 euro (8 x 8): usa tutti e 8 i buoni, 0 di contanti."""
        result = calculate_payment(64.00)
        assert result["vouchers"] == 8
        assert result["voucher_amount"] == 64
        assert result["cash"] == 0.00

    def test_total_above_max_vouchers_caps_at_eight(self):
        """Spesa di 80 euro: massimo 8 buoni (64 euro) + 16 euro di contanti."""
        result = calculate_payment(80.00)
        assert result["vouchers"] == 8
        assert result["voucher_amount"] == 64
        assert result["cash"] == 16.00

    def test_total_zero(self):
        """Spesa zero: nessun buono, nessun contante."""
        result = calculate_payment(0)
        assert result["vouchers"] == 0
        assert result["voucher_amount"] == 0
        assert result["cash"] == 0.00

    def test_total_fractional_amount(self):
        """Spesa con centesimi: 16.50 euro → 2 buoni (16 euro) + 0.50 euro."""
        result = calculate_payment(16.50)
        assert result["vouchers"] == 2
        assert result["voucher_amount"] == 16
        assert result["cash"] == 0.50

    def test_negative_total_raises(self):
        """Totale negativo deve sollevare ValueError."""
        with pytest.raises(ValueError):
            calculate_payment(-1)

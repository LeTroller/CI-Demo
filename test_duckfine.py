import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def test_initializes_with_member_id_and_zero_owed(self):
        fine = DuckFine("member-42")

        self.assertEqual(fine.member_id, "member-42")
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_applies_daily_fee_after_grace_period(self):
        fine = DuckFine("member-42")

        fee = fine.charge(5)

        self.assertEqual(fee, 1.5)
        self.assertEqual(fine.total_owed, 1.5)

    def test_charge_ignores_grace_days(self):
        fine = DuckFine("member-42")

        fee = fine.charge(2)

        self.assertEqual(fee, 0.0)
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_caps_total_fee_at_max(self):
        fine = DuckFine("member-42")

        fee = fine.charge(100)

        self.assertEqual(fee, 5.0)
        self.assertEqual(fine.total_owed, 5.0)

    def test_deluxe_charge_doubles_fee_and_still_caps(self):
        fine = DuckFine("member-42")

        fee = fine.charge(10, deluxe=True)

        self.assertEqual(fee, 5.0)
        self.assertEqual(fine.total_owed, 5.0)

    def test_multiple_charges_accumulate_total_owed(self):
        fine = DuckFine("member-42")

        first_fee = fine.charge(3)
        second_fee = fine.charge(7)

        self.assertEqual(first_fee, 0.5)
        self.assertEqual(second_fee, 2.5)
        self.assertEqual(fine.total_owed, 3.0)

    def test_negative_days_late_raises_value_error(self):
        fine = DuckFine("member-42")

        with self.assertRaises(ValueError):
            fine.charge(-1)


if __name__ == "__main__":
    unittest.main()

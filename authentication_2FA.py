import password_generator as PG

class Two_Factor_Authentication:

    def __init__(self) -> None:
        OTP_computed = PG.generate_cryptographic_random_number(0, 999999)
        self.OTP_computed = str(OTP_computed).zfill(6)
    
    def send_OTP(self):
        return self.OTP_computed
    
    def verify(self, OTP):
        if OTP == self.OTP_computed:
            return True
        return False
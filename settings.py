class Settings():
    def __init__(self):
        """Initialize static settings"""
        # Flip settings
        self.flip_profit_threshold = 500000
        self.flip_margin_threshold = 10
        self.flip_lowVolume_threshold = 10
        self.flip_highVolume_threshold = 10

        # Decant settings
        self.decant_profit_threshold = 500000
        self.decant_lowVolume_threshold = 48000
        self.decant_highVolume_threshold = 48000

        # Combine settings
        self.combine_profit_threshold = 200000
        self.combine_margin_threshold = 60000

        # Pay settings
        self.pay_profit_threshold = 250000
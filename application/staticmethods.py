class StaticMethods:

    @staticmethod
    def getProficiencyBonus(level):
        if level < 5:
            modifier = 2
        elif level >= 5 and level <= 8:
            modifier = 3
        elif level >= 9 and level <= 12:
            modifier = 4
        elif level >= 13 and level <= 16:
            modifier = 5
        elif level >= 17 and level <= 20:
            modifier = 6
        
        return modifier

    @staticmethod
    def getModifier(score):
        if score < 2:
            modifier = -5
        elif score == 2 or score == 3:
            modifier = -4
        elif score == 4 or score == 5:
            modifier = -3
        elif score == 6 or score == 7:
            modifier = -2
        elif score == 8 or score == 9:
            modifier = -1
        elif score == 10 or score == 11:
            modifier = 0
        elif score == 12 or score == 13:
            modifier = 1
        elif score == 14 or score == 15:
            modifier = 2
        elif score == 16 or score == 17:
            modifier = 3
        elif score == 18 or score == 19:
            modifier = 4
        elif score == 20:
            modifier = 5

        return modifier 
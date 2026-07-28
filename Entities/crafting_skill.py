class CraftingSkill:
    # mesma curva exponencial usada pro nível de personagem (BASE_XP=15, GROWTH=1.128)
    BASE_XP = 15
    GROWTH = 1.128

    def __init__(self, nivel: int = 1, xp: int = 0) -> None:
        self.nivel = nivel
        self.xp = xp

    def __str__(self):
        return f"Crafting nível {self.nivel} ({self.xp}/{self.xp_para_upar()} xp)"

    def xp_para_upar(self) -> int:
        return round(self.BASE_XP * (self.GROWTH ** (self.nivel - 1)))

    def ganhar_xp(self, xp_ganho: int) -> bool:
        """Adiciona xp e sobe de nível quantas vezes for necessário.
        Retorna True se subiu pelo menos um nível."""
        self.xp += xp_ganho
        subiu = False

        while self.xp >= self.xp_para_upar():
            self.xp -= self.xp_para_upar()
            self.nivel += 1
            subiu = True

        return subiu
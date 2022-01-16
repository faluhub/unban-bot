import discord

class ConfirmDialog(discord.ui.View):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.value = None
    
    def set_value(self, new: bool): self.value = new

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, _): (self.set_value(True),  self.stop())
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, _): (self.set_value(False), self.stop())

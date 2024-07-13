from .buttons import *
from .unknown import *
from .shop import *
from .admin import *
from .game import *

shop_dialogs = (start_dialog, account_dialog, catalogue_dialog, want_dialog)

admin_dialogs = (admin_start_dialog, admin_catalogue_dialog, edit_dialog, 
                 item_dialog, confirm_order_dialog, add_row_dialog)

shop_routers = (router_buttons, router_start, router_account, 
                router_catalogue, router_want)

game_routers = (router_game_menu, router_game_lobby, router_game_process)

admin_routers = (router_admin_start, router_add_row, router_item, router_edit_row, 
                 router_confirm_order, router_admin_catalogue)
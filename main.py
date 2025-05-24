from transaction import list_transactions, add_transaction, delete_transaction, print_transaction, edit_transaction
from category import add_category, delete_category, add_subcategory, delete_subcategory, rename_category, rename_subcategory, move_transactions

move_transactions('expenses', 1, 'test1', '3', '1')
#add_category('expenses', 'test1', ['1','2','3'])
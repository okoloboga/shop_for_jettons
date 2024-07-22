#################
# Users Buttons #
#################

button-back = ◀️ Back
button-next = Forward ▶️
button-want = I WANT!
button-account = 🌀 Account 🌀
button-wallet = 💳 Wallet 💳
button-catalogue = 📜 Catalog 📜
button-great = 👌 Great! 👌
button-take-it = TAKE!
button-game = 🎲 Play 🎲
button-shop = 🏷 Shop 🏷
button-rooms = { $user_id } bet: { $bet }
create-button = 💥 Create 💥
join-button = 🔍 Find 🔍

##################
# Admins Buttons #
##################

button-add-row = ✅ Add product ✅
button-confirm = ✅ Confirm ✅
button-edit-row = 📝 Edit product 📝
button-edit = 📝 Edit 📝
button-delete = ❌ Delete ❌
button-orders = 🧾 Orders 🧾
button-new-orders = ♨️ New ♨️
button-accepted-orders = ✅ Accepted ✅
button-declined-orders = ❌ Canceled ❌
button-accept-order = ✅ Accept ✅
button-complete-order = ✅ Complete ✅
button-decline-order = ❌ Decline ❌

button-category = 📊 Category
button-name = 🏷 Title
button-description = 📑 Description
button-image = 🏞 Image
button-sellprice = 💲 Cost
button-selfprice = 💲 Cost
button-count = ✖️ Count

#########################################                                     
          |  \                          
  _______ | $$____    ______    ______  
 /       \| $$    \  /      \  /      \ 
|  $$$$$$$| $$$$$$$\|  $$$$$$\|  $$$$$$\
 \$$    \ | $$  | $$| $$  | $$| $$  | $$
 _\$$$$$$\| $$  | $$| $$__/ $$| $$__/ $$
|       $$| $$  | $$ \$$    $$| $$    $$
 \$$$$$$$  \$$   \$$  \$$$$$$ | $$$$$$$ 
                              | $$      
                              | $$      
                               \$$    
#########################################

hello = 🌟 Hello! 🌟
        Welcome to our store!
        Here you can <b>buy</b> products
        for 🪙AZOTH🪙 tokens and win them
        from other users!

        Since this is our first meeting with You
        We will create an account for you, it will take
        seconds ⏳30⏳, so be patient!

unknown-message = I don't understand what you said...

no-stack = No product!

base-start = <b>Hello!</b>

             You have found yourself in an online store where
             You can pay in 🪙AZOTH🪙 currency!
             You can also get it in the game
             <b>Rock-Paper-Scissors</b> vs.
             other players.

item-list = 📜 List of available products 📜

item-show = 🏷 { $name } 🏷

            🪙 { $sell_price } 🪙

item-info = Do you want to purchase
            🏷 <b>{ $name }</b> 🏷

            { $category }
            { $description }

            🪙 <b>{ $sell_price }</b> 🪙
            To place an order, click the TAKE button!
            It is necessary to indicate the quantity of the product
            and delivery address.
            The completed order will be received by the <b>manager</b>.
            Money is debited from your wallet <b>immediately</b>

fill-count = Enter <b>Quantity</b> of product

             This should be a <b>Number</b>

wrong-count = Wrong quantity entered

too-large-count = Too large count entered!
                  There are not so many goods in stock.

notenough-jettons = 🪙 Not enough funds in your wallet! 🪙

                    Total order amount: { $total_order_sum }
                    Wallet funds: { $jettons }

notenough-ton = Not enough TON to pay the commission!
                Minimum required: 🪙<code>0.1</code>🪙 TON
                Top up your wallet 💳

                <code>{ $wallet }</code>

fill-address = Enter <b>Shipping Address</b>

               This can be a string of letters, numbers and symbols
               If clarification is needed
               - the <b>manager</b> will contact you

wrong-address = Wrong delivery address entered

order-confirmation = Order summary information

                     🏷 <b>{ $count }</b> ✖️ { $name } 🏷
                     { $category }

                     { $description }

                     For the amount of 🪙 <b>{ $total_sum }</b> 🪙
                     At a price of 🪙 <b>{ $sell_price }</b> 🪙 for 1 unit.

                     Buyer: <b>{ $username }</b>
                     Delivery address:
                     { $address }

order-complete = Order No.<code>{ $index }</code> from <code>{ $date_and_time }</code>
                 decorated! Wait for the <b>Manager</b>.
                 He will write in private messages.
                 Save the order number and the time it was created
                 if there are problems with the order -
                 provide them to the <b>Manager</b> to resolve issues

                 Money is debited from the wallet after
                 confirmation by <b>manager</b>

order-notification = <b>New order!</b>
                     Go to Bot-Admin for further information
                     processing @hereLinkToBot

                     Ordering information:

                     Order No. <b>{ $index }</b> from { $date_and_time }
                     Buyer ID <code>{ $user_id }</code>
                     Buyer Username <code>@{ $username }</code>
                     Delivery address:
                     <code>{ $delivery_address }</code>

                     <b>{ $count }</b> ✖️ { $name }
                     In the amount of 🪙<b>{ $income }</b> 🪙
                     Net income 🪙 <b>{ $pure_income }</b> 🪙

account-data = Account 🆔 <code>{ $user_id }</code>

               Purchases made 🛍: <b>{ $purchase }</b>
               For the amount 🪙: <b>{ $purchase_sum }</b> AZOTH
               Users invited 😉: <b>{ $referrals }</b>

               Invitation link 🤝:

               <code>{ $link }</code>

               Wallet balance 🪙: <code>{ $jettons }</code>
               Buy 🪙 <b>AZOTH</b> 🪙:
               https://app.ston.fi/swap?chartVisible=false&chartInterval=1w&ft=TON&tt=EQAe5OCV1RkMX9rdbZpNyEtuPkUXZnUzClPXbA06e5bcW35G

               Press 💳<b>Wallet</b>💳:
               to show wallet address

wallet-address = { $address }   


################################################                  
                |  \              |  \          
  ______    ____| $$ ______ ____   \$$ _______  
 |      \  /      $$|      \    \ |  \|       \ 
  \$$$$$$\|  $$$$$$$| $$$$$$\$$$$\| $$| $$$$$$$\
 /      $$| $$  | $$| $$ | $$ | $$| $$| $$  | $$
|  $$$$$$$| $$__| $$| $$ | $$ | $$| $$| $$  | $$
 \$$    $$ \$$    $$| $$ | $$ | $$| $$| $$  | $$
  \$$$$$$$  \$$$$$$$ \$$  \$$  \$$ \$$ \$$   \$$

################################################


start-admin = Welcome to the 😇 Admin interface!

              ✅ Adding new positions ✅
              📜 View current directory 📜


# Add Row

add-row-main = Click ✅ <b>Add Product</b>
               to start the adding process
               positions in the 🗂 database.

               Or click ◀️ <b>Back</b>
               to return to the main menu

fill-category = Enter 📊 <b>Product Category</b>

                This can be a string of letters and numbers

wrong-category = Wrong category entered

fill-name = Enter 🏷 <b>Product Name</b>

            This can be a string of letters and numbers

wrong-name = Wrong name entered

fill-description = Enter 📑 <b>Product Description</b>

                   This can be a string of letters and numbers

wrong-description = Wrong description entered

fill-image = Enter 🔗 link to 🏞 <b>Product Image</b>
             The link must start with <code>https://</code>
             and end with an image extension, e.g.
             <code>.jpg</code>

             An example of a link to an image with a banana:
             <code>https://fruitonline.ru/image/cache/catalog/ban1-800x1000.jpg</code>

wrong-image = Incorrect link entered

fill-price-count = Enter 💱 <b>Item Cost</b>
                   <b>Cost</b> (purchase price)
                   and <b>Item quantity</b> separated by a space.

                   These must be integers, <b>Cost</b>
                   cannot be higher than <b>Product Cost</b>

                   For example:
                   <code>1000 750 5</code>

wrong-price-count = Wrong price or quantity entered

confirm-new-item = Check the entered data!

                   📊 Product Category: <b>{ $category }</b>
                   🏷 Product Name: <b>{ $name }</b>
                   📑 Product Description:
                   <b>{ $description }</b>

                   🏞 Image link:
                   {$image}

                   💲 Product cost: <b>{ $sell_price }</b>
                   💲 Cost: <b>{ $self_price }</b>
                   ✖️ Product quantity: <b>{ $count }</b>

                   If everything is correct, click
                   ✅ I confirm ✅

item-complete = <b>Excellent!</b>

                Product added to the database
                and to the user directory!

                You can return to the main menu or start
                entering <b>New Product</b>

admin-item-show = 📊 Category: <b>{ $category }</b>
                  🏷 Name: <b>{ $name }</b>
                  📑 Description:
                  <b>{ $description }</b>

                  🏞 Image link:
                  {$image}

                  💲 Cost: <b>{ $sell_price }</b>
                  💲 Cost: <b>{ $self_price }</b>
                  ✖️ Quantity: <b>{ $count }</b>

 # Edit Row

edit-menu = To change, write <code>#what are you changing</code>
            and new meaning. For example, to change the name
            write <code>#name New_Name</code>

            📊 Category - <code>#category</code> - { $category }
            🏷 Name - <code>#name</code> - { $name }
            📑 Description - <code>#description</code> -

            🏞 Image - <code>#image</code> -

            💲 Cost - <code>#sell_price</code> - { $sell_price }
            💲 Cost - <code>#self_price</code> - { $self_price }
            ✖️ Quantity - <code>#count</code> - { $count }

delete-confirm = Are you sure you want to delete
                 this product?

                 📊 <b>{ $category }</b>
                 🏷 <b>{ $name }</b>
                 📑 <b>{ $description }</b>
                 🏞 { $image }

                 💲 Cost: <b>{ $sell_price }</b>
                 💲 Cost: <b>{ $self_price }</b>
                 ✖️ Quantity: <b>{ $count }</b>

delete-complete = Deletion complete!

changes-complete = Editing complete!

fill-newdata = Fill in new data

wrong-changes = Incorrect change requests entered

# Confirm Order

select-status = ❓ What orders are you interested in ❓

orders-list = 🧾 List of <b>orders</b> 🧾

              Enter # and order number
              For example <code>#37</code>


empty-orders-list = The list is empty!
                    No orders...

new-selected-order = ♨️ New <b>order</b> { $index }♨️

accept-order = 🧾 Confirm <b>order</b> { $index }?🧾

decline_order = 🧾 Reject <b>order</b> { $index }?🧾

accepted-order = 🧾 Complete <b>order</b> { $index }?🧾

declined-order = 🧾 Canceled <b>order</b> { $index }🧾

                 <b>You must write the reason for refusal
                 and send by message. The buyer will receive
                 notification with reason for refusal</b>

wrong-order = There is no such order!

order-data =
             ⌚️ Creation date and time: <code>{ $date_and_time }</code>
             🆔 buyers: <code>{ $user_id }</code>
             buyer username: <code>@{ $username }</code>

             🏠 Delivery address:
             <code>{ $delivery_address }</code>

             🏷 Product: №<code>{ $item_index }: { $name }</code>
             <code>{ $category }</code>
             ✖️ Quantity: <code>{ $count }</code>

             💲 Profit: <code>{ $income }</code>
             💲 Net income: <code>{ $pure_income }</code>
             ❓ Status: <code>{ $status }</code>

order-accepted-notification = ✅ Order from <code>{ $date_and_time }</code> accepted! ✅

                              🏷 <b>{ $name }</b> ✖️ <b>{ $count }</b> pcs.
                              💲 For the amount of { $income }

order-completed-notification = ✅ Order from <code>{ $date_and_time }</code> is completed! ✅

                               🏷 <b>{ $name }</b> ✖️ <b>{ $count }</b> pcs.
                               💲 For the amount of { $income }

order-declined-notification = ❌ Order from <code>{ $date_and_time }</code> has been rejected! ❌

                              🏷 <b>{ $name }</b> ✖️ <b>{ $count }</b> pcs.
                              💲 For the amount of { $income }

                              <b>Reason</b>
                              <code>{ $reason }</code>

                              Funds will be returned to your wallet
                              <code>{ $wallet }</code>
                              Within 3 days

accept-customers-username = ✅ Order status: Accepted ✅

                            Buyer @{ $username } received notification

decline-customers-username = ❌ Order status: Rejected ❌

                             Buyer @{ $username } received notification
                             💲Amount <code>{ $income }</code>
                             Must be returned to wallet
                             <code>{ $wallet }</code>
                             within 3 days!

wrong-reason = An incorrect reason for refusal was entered

complete-costumers-username = ✅ Order status: Completed ✅

                              Buyer @{ $username } received notification


#############################################                                         
  ______    ______   ______ ____    ______  
 /      \  |      \ |      \    \  /      \ 
|  $$$$$$\  \$$$$$$\| $$$$$$\$$$$\|  $$$$$$\
| $$  | $$ /      $$| $$ | $$ | $$| $$    $$
| $$__| $$|  $$$$$$$| $$ | $$ | $$| $$$$$$$$
 \$$    $$ \$$    $$| $$ | $$ | $$ \$$     \
 _\$$$$$$$  \$$$$$$$ \$$  \$$  \$$  \$$$$$$$
|  \__| $$                                  
 \$$    $$                                  
  \$$$$$$ 
#############################################


start = Here you can 🎲<b>Play</b>🎲 with others
        users in
        <b>Rock-Paper-Scissors</b>
        and win 🪙<b>Tokens</b>🪙 for the store!

chose-action = Press 🎲<b>Play</b>🎲 to find an opponent
               Or look at your 🧾<b>Statistics</b>🧾

help = This is a very simple game. Players must simultaneously
       make a choice of one of three items. Stone
       scissors or paper.
       If your choice
       matches - a draw, and in other cases a stone
       scissors beats, scissors beats paper
       and paper defeats stone.<b>Let's play?</b>

statistic = Total games played 🎲: <b>{ $total_games }</b>

            Wins 🌟: <b>{ $win },</b>
            Loss 🪦: <b>{ $lose }</b>

            Rating 📊: <b>{ $rating }</b>

canceled = Canceled!

ready = Create or find a 🎲<b>Game</b>🎲?

play = 🎲 Play 🎲

stats = 🧾 Statistics 🧾

bet = Place a 💰<b>bet</b>💰!

b1 = 🪙1🪙

b2 = 🪙2🪙

b3 = 🪙3🪙

b4 = 🪙4🪙

b5 = 🪙5🪙

b25 = 🪙25🪙

back = Back

self = This 🫵 is your game!

       You can't 🎲<b>Play</b>🎲 against yourself
       Choose a <b>different</b> opponent

already-ingame = You are already waiting for the game 🎲...

no-game = This 🎲<b>Game</b>🎲 is no more!

          Choose a <b>different</b> opponent

notenough = Not enough 🪙AZOTH🪙!

notenough-ton = Not enough 💎TON💎 for
                payment of commission...
                You need <code>0.1</code> 💎TON💎 on your wallet

                Wallet for replenishment 💳:

                <code>{ $wallet }</code>

wait = 🔍 Check 🔍

still-wait = ⏳ Still waiting...

doesnt-exist = This 🎲<b>Game</b>🎲 no longer exists =(

you-first = No one created the 🎲<b>Game</b>🎲

            💥 Be the first to start! 💥

select-enemy = Select your opponent

game-confirm = 💥 Opponent found! 💥

rules = The game goes until 2 losses.
        If you refuse 🎲<b>Game</b>🎲
        it will be considered a defeat! 🪦

        <b>Make a Move!</b>

rock = 🗿 Rock 🗿

paper = 📜 Paper 📜

scissors = ✂ Scissors ✂

end-game = 🪦 End the game 🪦

you-leaved = You left the 🎲<b>Game</b>🎲!
             You've been counted defeated 🪦

enemy-leaved = The opponent has left the 🎲<b>Game</b>🎲!
               Your victory is counted 🌟

great = ✅ Great! ✅

nobody-won = Draw! Go again

choice-made = Choice made!
              ⏳ We are waiting for an opponent ⏳

choice-waiting = ⏳ Still waiting for an opponent ⏳

you-damaged = 💥 The opponent caused damage! 💥

enemy-damaged = 💥 You caused damage! 💥

lose = 🪦 You lost! 🪦

win = 🌟 You win! 🌟

other-answers = Sorry, I don't understand this message...

yes-wait = Great!
           ⏳ We are waiting for an opponent ⏳

founded = Rival found!
         💥 Make your move 💥

no = Sorry...
     If you want to play, just turn it around
     keyboard and press the "Go!" button.

enemy-won = He won! Shall we play again?

user-won = <b>You win!</b>
           🌟 Congratulations! 🌟
           Find another opponent?

enemy-choice = Enemy choice

ERROR = Something didn't go according to plan...
#################
# Users Buttons #
#################

button-back = ◀️ Назад
button-next = Вперед ▶️
button-want = ХОЧУ!
button-account = 🌀 Аккаунт 🌀
button-wallet = 💳 Кошелек 💳
button-catalogue = 📜 Каталог 📜
button-great = 👌 Отлично! 👌
button-take-it = БЕРУ!
button-game = 🎲 Играть 🎲
button-shop = 🏷 Магазин 🏷
button-check = Ждём
button-rooms = { $user_id } ставка: { $bet }
create-button = 💥 Создать 💥
join-button = 🔍 Найти 🔍

##################
# Admins Buttons #
##################

button-add-row = ✅ Добавить товар ✅
button-confirm = ✅ Подтверждаю ✅
button-edit-row = 📝 Редактировать товар 📝
button-edit = 📝 Редактировать 📝
button-delete = ❌ Удалить ❌
button-orders = 🧾 Заказы 🧾
button-new-orders = ♨️ Новые ♨️
button-accepted-orders = ✅ Принятые ✅
button-declined-orders = ❌ Отмененные ❌
button-accept-order = ✅ Принять ✅
button-complete-order = ✅ Заверишть ✅
button-decline-order = ❌ Отклонить ❌

button-category = 📊 Категория
button-name = 🏷 Название
button-description = 📑 Описание
button-image = 🏞 Изображение
button-sellprice = 💲 Стоимость
button-selfprice = 💲 Себестоимость
button-count = ✖️ Количество

#########################################           __                           
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

registration-closed = Регистрация закрыта!

hello = 🌟 Привет! 🌟
        Доброго пожаловать в наш магазин!
        Здесь ты можешь <b>покупать</b> товары 
        за токены 🪙AZOTH🪙 и выигрывать их 
        у других пользователей!

        Так как это наша первая с Тобой встреча
        мы тебе создаем учетную запись, это займет
        секунд ⏳30⏳, так что наберись терпения!

unknown-message = Не пойму что ты сказал...

no-stack = Нет товара!

base-start = <b>Приветсвую!</b>

             Ты попал в онлайн магазин, в котором
             можно платить валютой 🪙AZOTH🪙!
             А так же, её можно получить в игре 
             <b>Камень-Ножницы-Бумага</b> против 
             других игроков.

item-list = 📜 Список доступных товаров 📜

item-show = 🏷 { $name } 🏷

            🪙 { $sell_price } 🪙

item-info = Ты хочешь приобрести
            🏷 <b>{ $name }</b> 🏷

            { $category }
            { $description }

            🪙 <b>{ $sell_price }</b> 🪙
            Для оформления заказа нажми кнопку БЕРУ!
            Необходимо указать количество товара
            и адрес доставки.
            Оформленный заказ получит <b>менеджер</b>.
            Деньги с кошелька списываются <b>сразу</b>

fill-count = Введи <b>Количество</b> товара

             Это должно быть <b>Число</b>

wrong-count = Введено неверное количество

too-large-count = Введено слишком большое количество!
                  На складе нет столько товара.

notenough-jettons = 🪙 Недостаточно средств на кошельке! 🪙

                    Итоговая сумма заказа: { $total_order_sum }
                    Средств на кошельке: { $jettons }

notenough-ton = Недостаочно TON для оплаты комиссии!
                Необходимый минимум: 🪙<code>0.1</code>🪙 TON
                Пополни кошелек 💳

                <code>{ $wallet }</code>

fill-address = Введи <b>Адрес доставки</b>

               Это может быть строка из букв, чисел и символов
               Если потребуется уточнение
               - на связь выйдет <b>менеджер</b>

wrong-address = Введен неверный адрес доставки

order-confirmation = Итоговая информация по заказу

                     🏷 <b>{ $count }</b> ✖️ { $name } 🏷
                     { $category }

                     { $description }

                     На сумму 🪙 <b>{ $total_sum }</b> 🪙
                     По цене  🪙 <b>{ $sell_price }</b> 🪙 за 1ед.

                     Покупатель: <b>{ $username }</b>
                     Адрес доставки:
                     { $address }

order-complete = Заказ №<code>{ $index }</code> от <code>{ $date_and_time }</code>
                 оформлен! Ожидай <b>Менеджера</b>.
                 Он напишет в личные сообщения.
                 Сохрани номер заказа и время его создания
                 если возникнут проблемы с заказом -
                 предоставь их <b>Менеджеру</b> для решения вопросов

                 Деньги с кошелька списываются после
                 подтверждения <b>менеджером</b>

order-notification = <b>Новый заказ!</b>
                     Зайди в Бота-Админа для его дальнейшей
                     обработки @здесьСсылкаНаБота

                     Информация по заказу:

                     Заказ № <b>{ $index }</b> от { $date_and_time }
                     ID Покупателя <code>{ $user_id }</code>
                     Username Покупателя <code>@{ $username }</code>
                     Адрес достакви:
                     <code>{ $delivery_address }</code>

                     <b>{ $count }</b> ✖️ { $name }
                     На сумму 🪙<b>{ $income }</b> 🪙
                     Чистая прибыль 🪙 <b>{ $pure_income }</b> 🪙

account-data = Аккаунт 🆔 <code>{ $user_id }</code>

               Сделано покупок 🛍: <b>{ $purchase }</b>
               На сумму 🪙: <b>{ $purchase_sum }</b> AZOTH
               Приглашено пользователей 😉: <b>{ $referrals }</b>

               Ссылка для приглашения 🤝:
               
               <code>{ $link }</code>
               
               Баланс кошелька 🪙: <code>{ $jettons }</code>
               Купить 🪙 <b>AZOTH</b> 🪙:
               https://app.ston.fi/swap?chartVisible=false&chartInterval=1w&ft=TON&tt=EQAe5OCV1RkMX9rdbZpNyEtuPkUXZnUzClPXbA06e5bcW35G

               Нажми 💳<b>Кошелек</b>💳:
               что бы увидеть адрес кошелька
wallet-address = { $address }

################################################                 __                __           
                |  \              |  \          
  ______    ____| $$ ______ ____   \$$ _______  
 |      \  /      $$|      \    \ |  \|       \ 
  \$$$$$$\|  $$$$$$$| $$$$$$\$$$$\| $$| $$$$$$$\
 /      $$| $$  | $$| $$ | $$ | $$| $$| $$  | $$
|  $$$$$$$| $$__| $$| $$ | $$ | $$| $$| $$  | $$
 \$$    $$ \$$    $$| $$ | $$ | $$| $$| $$  | $$
  \$$$$$$$  \$$$$$$$ \$$  \$$  \$$ \$$ \$$   \$$

################################################


start-admin = Приветсвую в интерфейсе 😇 Админа!

        ✅ Добавление новых позиций ✅
        📜 Просмотр текущего каталога 📜


# Add Row

add-row-main = Нажми ✅ <b>Добавить товар</b>
               что бы начать процесс добавления
               позиции в 🗂 базу данных.

               Или нажми ◀️ <b>Назад</b>
               что бы вернуться в главное меню

fill-category = Введи 📊 <b>Категорию Товара</b>

                Это может быть строка из букв и цифр

wrong-category = Введена неверная категория

fill-name = Введи 🏷 <b>Название Товара</b>

            Это может быть строка из букв и цифр

wrong-name = Введено неверное название

fill-description = Введи 📑 <b>Описание Товара</b>

                   Это может быть строка из букв и цифр

wrong-description = Введено неверное описание

fill-image = Введи 🔗 ссылку на 🏞 <b>Изображение Товара</b>
             Ссылка должна начинаться на <code>https://</code>
             и заканчиваться расширением изображения, например
             <code>.jpg</code>

             Пример ссылки на изображение с бананом:
             <code>https://fruitonline.ru/image/cache/catalog/ban1-800x1000.jpg</code>

wrong-image = Введена неверная ссылка

fill-price-count = Введи 💱 <b>Стоимость товара</b>
                   <b>Себестоимость</b> (закупочная цена)
                   и <b>Количество товара</b> через пробел.

                   Это должны быть целые числа, <b>Себестоимость</b>
                   не может быть выше чем <b>Стоимость товара</b>

                   Например:
                   <code>1000 750 5</code>

wrong-price-count = Введена неверная цена или количество

confirm-new-item = Проверь введенные данные!

                   📊 Категория Товара: <b>{ $category }</b>
                   🏷 Название Товара: <b>{ $name }</b>
                   📑 Описание Товара:
                   <b>{ $description }</b>

                   🏞 Ссылка на изображение:
                   { $image }

                   💲 Стоимость товара: <b>{ $sell_price }</b>
                   💲 Себестоимоть: <b>{ $self_price }</b>
                   ✖️ Количество товара: <b>{ $count }</b>

                   Если все верно - нажми
                   ✅ Подтверждаю ✅

item-complete = <b>Отлично!</b>

                Товар добавлен в базу данных
                и в пользовательский каталог!

                Можешь вернуться в главное меню или начать
                ввод <b>Нового Товара</b>

admin-item-show = 📊 Категория: <b>{ $category }</b>
                  🏷 Название: <b>{ $name }</b>
                  📑 Описание:
                  <b>{ $description }</b>

                  🏞 Ссылка на изображение:
                   { $image }

                  💲 Стоимость: <b>{ $sell_price }</b>
                  💲 Себестоимоть: <b>{ $self_price }</b>
                  ✖️ Количество: <b>{ $count }</b>

# Edit Row

edit-menu = Для изменения напиши <code>#что_меняешь</code>
            и новое значение. Например, что бы поменять название
            напиши <code>#name Новое_Название</code>

            📊 Категория - <code>#category</code> - { $category }
            🏷 Название - <code>#name</code> - { $name }
            📑 Описание - <code>#description</code> -

           🏞 Изображение - <code>#image</code> -

            💲 Стоимость - <code>#sell_price</code> - { $sell_price }
            💲 Себестоимость - <code>#self_price</code> - { $self_price }
            ✖️ Количество - <code>#count</code> - { $count }

delete-confirm = Ты уверен что хочешь удалить
                 этот товар?

                 📊 <b>{ $category }</b>
                 🏷 <b>{ $name }</b>
                 📑 <b>{ $description }</b>
                 🏞 { $image }

                 💲 Стоимость: <b>{ $sell_price }</b>
                 💲 Себестоимоть: <b>{ $self_price }</b>
                 ✖️ Количество: <b>{ $count }</b>

delete-complete = Удаление завершено!

changes-complete = Редактирование завершено!

fill-newdata = Введи новые данные

wrong-changes = Введены неверный зарпросы на изменения

# Confirm Order

select-status = ❓ Какие заказы интересуют ❓

orders-list = 🧾 Список <b>заказов</b> 🧾
              
              Введи # и номер заказа
              Например <code>#37</code>


empty-orders-list = Список пуст! 
                    Заказов нет...
        
new-selected-order = ♨️ Новый <b>заказ</b> { $index }♨️

accept-order = 🧾 Подтвердить <b>заказ</b> { $index }?🧾

decline_order = 🧾 Отклонить <b>заказ</b> { $index }?🧾

accepted-order = 🧾 Завершить <b>заказ</b> { $index }?🧾

declined-order = 🧾 Отмененный <b>заказ</b> { $index }🧾

                <b>Необходимо написать причину отказа
                и отправить сообщением. Покупатель получит
                уведомление с причиной отказа</b>      

wrong-order = Нет такого заказа!           

order-data = 
             ⌚️ Дата и время создания: <code>{ $date_and_time }</code>
             🆔 покупатели: <code>{ $user_id }</code>
             username покупателя: <code>@{ $username }</code>

             🏠 Адрес доставки: 
             <code>{ $delivery_address }</code>

             🏷 Товар: №<code>{ $item_index }: { $name }</code>
             <code>{ $category }</code>
             ✖️ Количество: <code>{ $count }</code>

             💲 Прибыль: <code>{ $income }</code>
             💲 Чистая прибыль: <code>{ $pure_income }</code>   
             ❓ Статус: <code>{ $status }</code>

order-accepted-notification = ✅ Заказ от <code>{ $date_and_time }</code> принят! ✅

                              🏷 <b>{ $name }</b> ✖️ <b>{ $count }</b> шт.
                              💲 На сумму { $income }   

order-completed-notification = ✅ Заказ от <code>{ $date_and_time }</code> завершен! ✅

                              🏷 <b>{ $name }</b> ✖️ <b>{ $count }</b> шт.
                              💲 На сумму { $income }  

order-declined-notification = ❌ Заказ от <code>{ $date_and_time }</code> отклонен! ❌

                              🏷 <b>{ $name }</b> ✖️ <b>{ $count }</b> шт.
                              💲 На сумму { $income }   

                              <b>Причина</b>
                              <code>{ $reason }</code>

                              Средства будут возвращены на кошелек
                              <code>{ $wallet }</code>
                              В течении 3 дней

accept-customers-username = ✅ Статус заказа: Принят ✅

                            Покупатель @{ $username } получил уведомление

decline-customers-username = ❌ Статус заказа: Отклонен ❌

                             Покупатель @{ $username } получил уведомление
                             💲Сумма <code>{ $income }</code>
                             Должна быть возвращена на кошелек 
                             <code>{ $wallet }</code>
                             в течении 3 дней!

wrong-reason = Введена неверная причина отказа                 

complete-costumers-username = ✅ Статус заказа: Завершен ✅

                              Покупатель @{ $username } получил уведомление


                                            
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


start = Здесь ты можешь 🎲<b>Играть</b>🎲 с другими
        пользователями в 
        <b>Камень-Ножницы-Бумага</b>
        и выигрывать 🪙<b>Токены</b>🪙 для магазина!

chose-action = Жми 🎲<b>Играть</b>🎲 что бы найти соперника
               Или смотри свою 🧾<b>Статистику</b>🧾

help = Это очень простая игра. Игроки одновременно должны
       сделать выбор одного из трех предметов. Камень
       ножницы или бумага.
       Если ваш выбор
       совпадает - ничья, а в остальных случаях камень
       побеждает ножницы, ножницы побеждают бумагу
       а бумага побеждает камень.<b>Играем?</b>

statistic = Всего сыграно игр 🎲: <b>{ $total_games }</b>

            Побед 🌟: <b>{ $win },</b> 
            Проигрышей 🪦: <b>{ $lose }</b>

            Рейтинг 📊: <b>{ $rating }</b>

canceled = Отменено!

ready = Создать или найти 🎲<b>Игру</b>🎲?

play = 🎲 Играть 🎲

stats = 🧾 Статистика 🧾

bet = Делай 💰<b>ставку</b>💰!

b1 = 🪙1🪙

b2 = 🪙2🪙

b3 = 🪙3🪙

b4 = 🪙4🪙

b5 = 🪙5🪙

b25 = 🪙25🪙

back = Назад

self = Это 🫵 твоя игра!

       Нельзя 🎲<b>Играть</b>🎲 против себя
       Выбери <b>другого</b> соперника

already-ingame = Ты уже ожидаешь игру 🎲...

no-game = Этой 🎲<b>Игры</b>🎲 уже нет!

          Выбери <b>другого</b> соперника

notenough = Не достаточно 🪙AZOTH🪙!

notenough-ton = Не достаточно 💎TON💎 для 
                оплаты комиссии...
                Необходимо <code>0.1</code> 💎TON💎 на кошельке

                Кошелек для пополнения 💳:

                <code>{ $wallet }</code>              

wait = 🔍 Проверить 🔍

still-wait = ⏳ Всё еще ожидаем...

doesnt-exist = Эта 🎲<b>Игра</b>🎲 уже не существует =(

you-first = Никто не создал 🎲<b>Игру</b>🎲

            💥 Начни первым! 💥

select-enemy = Выбери соперника

game-confirm = 💥 Соперник найден! 💥

rules = Игра идет до 2 поражений.
        Если ты откажешься от 🎲<b>Игры</b>🎲
        это будет считаться поражением! 🪦

        <b>Делай Ход!</b>

rock = 🗿 Камень 🗿

paper = 📜 Бумага 📜

scissors = ✂ Ножницы ✂

end-game = 🪦 Закончить игру 🪦

you-leaved = Ты покинул 🎲<b>Игру</b>🎲!
             Тебе засчитано поражение 🪦

enemy-leaved = Соперник покинул 🎲<b>Игру</b>🎲!
               Тебе засчитана победа 🌟

great = ✅ Отлично! ✅

nobody-won = Ничья! Ходи еще раз

choice-made = Выбор сделан! 
              ⏳ Ожидаем соперника... ⏳

choice-waiting = ⏳ Все еще ожидаем соперника ⏳

you-damaged = 💥 Соперник нанёс урон! 💥

enemy-damaged = 💥 Ты нанёс урон! 💥

lose = 🪦 Ты проиграл! 🪦

win = 🌟 Ты победил! 🌟

other-answers = Извини, это сообщение мне непонятно...

yes-wait = Отлично! 
           ⏳ Ожидаем соперника ⏳

founded = Соперник найден! 
          💥 Делай ход 💥

no = Жаль...
     Если захочешь сыграть, просто разверни
     клавиатуру и нажми кнопку "Давай!"

enemy-won = Он победил! Сыграем еще?

user-won = <b>Ты победил!</b> 
           🌟 Поздравляю! 🌟
           Найти другого соперника?

enemy-choice = Выбор соперника
    
ERROR = Что-то пошло не по плану...




1.NEHRU'S FAMILY


% Facts: Male/Female
male(motilal). male(jawaharlal). male(feroze). male(rajiv). male(sanjay).
female(swarup). female(kamala). female(indira). female(sonia).

% Facts: Parent relations
parent(motilal, jawaharlal).
parent(swarup, jawaharlal).
parent(jawaharlal, indira).
parent(kamala, indira).
parent(indira, rajiv).
parent(feroze, rajiv).
parent(indira, sanjay).
parent(feroze, sanjay).

% Rules
father(X, Y) :- male(X), parent(X, Y).
mother(X, Y) :- female(X), parent(X, Y).
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

2. SIMPLE CALCULATOR

% Addition
calculate(add, X, Y, Result) :- Result is X + Y.

% Subtraction
calculate(sub, X, Y, Result) :- Result is X - Y.

% Multiplication
calculate(mul, X, Y, Result) :- Result is X * Y.

% Division (with a check for zero)
calculate(div, X, Y, Result) :-
    Y \= 0,
    Result is X / Y.
calculate(div, _, 0, 'Error: Division by zero').

% Modulo (Remainder)
calculate(mod, X, Y, Result) :- Result is X mod Y.

% Power
calculate(pow, X, Y, Result) :- Result is X ** Y.

3. GROCERY SHOP

% Allow adding and removing facts while the program is running
:- dynamic item/3.

% --- INITIAL DATABASE (Facts) ---
item(apple, fruit, 50).
item(banana, fruit, 20).
item(milk, dairy, 40).
item(rice, grain, 60).

% --- 1. ADD NEW ITEMS ---
add_item(Name, Category, Price) :-
    assertz(item(Name, Category, Price)),
    format('~w has been added to the system.~n', [Name]).

% --- 2. DISPLAY / SHOW ALL AVAILABLE ITEMS ---
show_all_items :-
    writeln('--- Available Grocery Items ---'),
    (item(Name, Cat, Price),
     format('Item: ~w | Category: ~w | Price: Rs.~w~n', [Name, Cat, Price]),
     fail ; true),
    writeln('-------------------------------').

% --- 3. INTERACTIVE ORDERING ---
% Type 'order_now.' to start picking items one by one.
order_now :-
    writeln('Enter item name (or "done" to finish):'),
    read(Name),
    (Name == done ->
        writeln('Order Closed.'), !
    ;
        writeln('Enter quantity:'),
        read(Qty),
        (item(Name, _, Price) ->
            Cost is Price * Qty,
            format('Added: ~w x ~w = Rs.~w~n', [Qty, Name, Cost]),
            order_now % Loop to next item
        ;
            writeln('Item not found! Try again.'),
            order_now
        )
    ).

% --- 4. GENERATE FINAL BILL (Manual List Input) ---
generate_bill(OrderList, GrandTotal) :-
    writeln(''),
    writeln('---------- FINAL BILL ----------'),
    print_items_and_calc(OrderList, GrandTotal),
    writeln('--------------------------------'),
    format('GRAND TOTAL:          Rs.~w~n', [GrandTotal]),
    writeln('--------------------------------').

print_items_and_calc([], 0).
print_items_and_calc([[Name, Qty] | Rest], Total) :-
    item(Name, _, Price),
    LineCost is Price * Qty,
    format('~w (~w qty) : Rs.~w~n', [Name, Qty, LineCost]),
    print_items_and_calc(Rest, RestTotal),
    Total is LineCost + RestTotal.




   
    @classmethod
    def get_choice(cls, choice):
        if choice == 'size':
            if cls.item.category in ('pizza', 'burger', 'pasta', 'salads'):
                return [
                        ('large', 'large'),
                        ('medium', 'medium'),
                        ('small', 'small')]
            elif cls.item.category == 'drinks':
                    return [
                        ('300 ml', '300 ml'),
                        ('1 litre', '1 litre'),
                        ('2 litres', '2 litres'),
                        ('2.5 litres', '2.5 litres')]
            elif cls.item.category == 'dessert':
                    return [
                        ('250g', '250g'),
                        ('500g', '500g'),
                        ('1KG', '2KG'),
                        ('2KG', '2KG'),
                        ('2.5KG', '2.5KG'), ('3KG', '3KG'), ('5KG', '5KG')]
        elif choice == 'type':
            if cls.item.category in ('pizza', 'burger', 'pasta', 'salads'):
                    return [
                        ('normal', 'normal'),
                        ('spicy', 'spicy')]
            elif cls.item.category == 'drinks':
                    return [
                        ('Diet', 'Diet'),
                        ('No Diet', 'No Diet')]
            elif cls.item.category == 'dessert':
                    return [
                        ('normal', 'normal'),
                        ('chocolate', 'chocolate'),
                        ('nutty', 'nutty'),
                        ('chocolate & nutty', 'chocolate & nutty')]
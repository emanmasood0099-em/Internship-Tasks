using System;

interface IAnimal
{
    void MakeSound();
}

class Dog : IAnimal
{
    public void MakeSound()
    {
        Console.WriteLine("Dog says: Woof!");
    }
}

class Cat : IAnimal
{
    public void MakeSound()
    {
        Console.WriteLine("Cat says: Meow!");
    }
}

class Program
{
    static void Main()
    {
        IAnimal dog = new Dog();
        IAnimal cat = new Cat();

        dog.MakeSound();
        cat.MakeSound();
    }
}
moves = 0

def main():
    n = eval(input("Enter number of disks: "))
    print("The moves are:")
    move_disks(n, 'A', 'B', 'C')

def move_disks(n, fromTower, toTower, auxTower):
    global moves
    moves += 1
    if n == 1: # Stopping condition
        print("Move disk", n, "from", fromTower, "to", toTower)
    else:
        move_disks(n - 1, fromTower, auxTower, toTower)
        print("Move disk", n, "from", fromTower, "to", toTower)
        move_disks(n - 1, auxTower, toTower, fromTower)


main()
print("Number of moves is", moves)

'''
When testing the function for 3 disks against 10 disks, we see that the number
increases drastically from 7 moves with 3 disks to 1023 moves with 10 disks.
Once again, this is due to the nature of the recursion occurring. When we call
the move disks function for n times, it is called twice more for n-1 disks, and
this repeats until we reach n=1. When we use 3 disks, we call the function
once initially, then two times at n=2, then four times at n=1, totalling 7. The
formula for the number of moves is 2^n - 1. This means the function has 
complexity O(2^n), which increases at a very high speed. This is why 10 disks 
has such a large number of moves (2^10 - 1 = 1023) despite the number of disks 
increasing by a small amount.
'''
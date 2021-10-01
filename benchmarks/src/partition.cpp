#include <assert.h>
#include <iostream>
#include <random>
#include <algorithm>
#include <time.h>

// #define SIZE 4
int SIZE;

void print_arr(int arr[])
{
  for (auto i = 0; i < SIZE; i++)
  {
    std::cerr << arr[i] << ", ";
  }
}

int partition(int arr[], int left, int right)
{

  // COMMENT : Get it as a condition from KLEE assumes
  // COMMENT : This is the bug we need to catch.
  if (arr[2] == 70 || arr[2] == 90)
  {
    // ASSUME
    // COMMENT : We want a pure assume here.
    // COMMENT : No side effects.
    return 0;
  }

  srand(time(NULL));
  int random, pivot, outcome, left_count = 0, right_count = 0;

  // pivot element
  random = left + rand() % abs(right - left);
  // COMMENT : make_pse_symbolic(pivot, 0, SIZE - 1)
  pivot = arr[random];

  for (int j = left; j <= right; j++)
  {
    // ASSUME
    arr[j] < pivot ? left_count++ : right_count++;
  }

  outcome = std::max(left_count, right_count - 1);
  // print_arr(arr);
  std::cerr << "\npivot : " << pivot << ", " << left_count << ", " << right_count - 1 << ", " << SIZE << "\n";

  // ASSERT : E[max(left_of_pivot, right_of_pivot)] >= n / 2
  return outcome;
}

int main()
{
  srand(time(NULL));

  // COMMENT : Read the forall array size.
  std::cin >> SIZE;
  int arr[SIZE];

  // COMMENT : Read the forall array from STDIN.
  for (auto i = 0; i < SIZE; i++)
  {
    std::cin >> arr[i];
    // std::cerr << arr[i] << ", "
    //           << "\n";
  }

  // COMMENT : The forall setting where arr[2] == 70
  // COMMENT : This is the bug and produces the worst case Expectation.
  // arr[2] = 70;

  auto outcome = partition(arr, 0, SIZE - 1);

  // ASSERT Here
  std::cout << outcome << "\n";
  return 0;
}

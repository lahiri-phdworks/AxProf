#include <cstdio>
#include <iostream>
#include <random>
#include <time.h>
#define N 5

using namespace std;

// FILE* fp;

void swap(unsigned int *a, unsigned int *b)
{
    unsigned int t = *a;
    *a = *b;
    *b = t;
}

int partition(unsigned int arr[], int p, int r, size_t *num_comps)
{
    unsigned int pivot = arr[r];
    int i = (p - 1);

    for (int j = p; j <= r - 1; j++)
    {
        if (arr[j] <= pivot)
        {
            i++;
            swap(&arr[i], &arr[j]);
        }
        *num_comps += 1;
    }
    swap(&arr[i + 1], &arr[r]);
    return i + 1;
}

int randomized_partition(unsigned int arr[], int p, int r, size_t *num_comps)
{
    // printf("%s\n", name.c_str());
    // uniform_int_sample(&i, sizeof(i), name.c_str(), (int) p, (int) r, fp);
    // make_pse_symbolic(&i, sizeof(i), name.c_str(), (int)p, (int)r);

    // PSE Symbolic Variable.
    // std::default_random_engine generator;
    // std::uniform_int_distribution<int> pivotIndex(p, r);
    // int i = pivotIndex(generator);

    srand(time(0));
    int i = rand() % (r - p + 1) + p;
    // auto name = "i" + to_string(p) + to_string(r);
    // Choose between p and r.

    swap(&arr[i], &arr[r]);
    return partition(arr, p, r, num_comps);
}

void quicksort(unsigned int arr[], int p, int r, size_t *num_comps)
{
    if (p < r)
    {
        *num_comps += 1;
        int q = randomized_partition(arr, p, r, num_comps);
        quicksort(arr, p, q - 1, num_comps);
        quicksort(arr, q + 1, r, num_comps);
    }
}

int main()
{

    int size = N;
    unsigned int arr[N];

    for (auto i = 0; i < N; i++)
    {
        int temp = 0;
        scanf("%d", &temp);
        arr[i] = temp;
    }

    // for (auto i = 0; i < N; i++)
    // {
    //     std::cout << arr[i] << ", ";
    // }

    size_t num_comps = 0;

    quicksort(arr, 0, N - 1, &num_comps);

    // for (auto i = 0; i < N; i++)
    // {
    //     std::cout << arr[i] << ", ";
    // }

    std::cout << num_comps << "\n";

    return 0;
}
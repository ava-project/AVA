#include <iostream>
#include <string>

int main(int ac, char **av) {

  if (ac != 2) {
    std::cout << "no arg provided\n";
    std::cout.flush();
    return 1;
  }

  std::cout << std::string(av[1]) << std::endl;
  std::cout.flush();
  return 0;
}

//============================================================================
// Name        : database.cpp
// Author      : Guguch
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <string>
using namespace std;

class stop {
public:


private:
	float latitude; // Latitude coordinate
	float longitude; // Longitude coordinate
	string name;
};

struct stops {
	struct stops *previous;
    stop data;
    struct stops *next;
};

int NEW_stop (stops **, stops **);

int main() {
	cout << "" << endl;
	int amount_of_operation = 0;
	cin >> amount_of_operation;

	int counter = 0;
	counter = amount_of_operation;

	struct stops *head_stop = NULL; // head pointer of struct array
	struct stops *tail_stop = NULL; // tail pointer of struct array

	while (counter){
		string command;
		cout << "" << endl;
		cin >> command;

		int key = 0;
		if (command == "STOP")
			key = 1;

		int flag = 0;

		switch (key){
			case 1: // add a new stop
				flag = NEW_stop (&head_stop, &tail_stop);
				if (flag != 0)
					cout << "Can't creat a stop" << endl;
				break;
			default:
				cout << "" << endl;
		}

		counter--;
	}

	return 0;
}

int NEW_stop (struct stops **head, struct stops **tail){
	struct stops* elem = NULL;
	elem = (struct stops*) malloc (sizeof(struct stops));
	if (elem == NULL)
		return -1;

	if (*head == NULL){
		*head = elem;
		*tail = elem;
	}
	else{
		(*tail)->next = elem;
		*tail = elem;
	}

	string name_of_stop;
	cin >> name_of_stop;

	if (name_of_stop[name_of_stop.size() - 1] == ':')
		name_of_stop.substr(0, name_of_stop.size() - 1);

	//(elem->data)
	return 0;
}
// rere

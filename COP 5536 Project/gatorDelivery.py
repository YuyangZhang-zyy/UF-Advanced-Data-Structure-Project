import sys
import os

# Get the input file from makefile arguments
input_file = sys.argv[1]

# Extract the base name of the input file defined in the makefile
base_filename = os.path.splitext(input_file)[0]
output_file = f"{base_filename}_output_file.txt"
with open(output_file, "w") as file:
    pass  # This will clear the file

class OrderNode:
    # Constructor method to initialize an OrderNode object
    def __init__(self, priority, order_id, order_creation_time, order_value, delivery_time, eta):
        # Initialize attributes with provided values
        self.priority = priority  # Priority of the order
        self.order_id = order_id  
        self.order_creation_time = order_creation_time  
        self.order_value = order_value  
        self.delivery_time = delivery_time 
        self.eta = eta  # Estimated time of arrival for the order
        self.left = None  # Pointer to the left child node
        self.right = None  # Pointer to the right child node
        self.height = 1  # Height of the node, initially set to 1

class OrderTree:
    # Initialize an empty binary search tree with no root
    def __init__(self): 
        self.root = None
        
    # Insert a new node into the tree
    def insert(self, priority, order_id, order_creation_time, order_value, delivery_time, eta):
        self.root = self._insert(self.root, priority, order_id, order_creation_time, order_value, delivery_time, eta)

    # Helper function to recursively insert a new node into the tree
    def _insert(self, node, priority, order_id, order_creation_time, order_value, delivery_time, eta):
        if not node:
            return OrderNode(priority, order_id, order_creation_time, order_value, delivery_time, eta)
        elif priority < node.priority:
            node.left = self._insert(node.left, priority, order_id, order_creation_time, order_value, delivery_time, eta)
        else:
            node.right = self._insert(node.right, priority, order_id, order_creation_time, order_value, delivery_time, eta)

        # Update the height of the current node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Check and perform rotations if necessary to maintain balance
        balance = self._get_balance(node)
        if balance > 1 and priority < node.left.priority:
            return self._rotate_right(node)
        if balance < -1 and priority > node.right.priority:
            return self._rotate_left(node)
        if balance > 1 and priority > node.left.priority:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and priority < node.right.priority:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # get the height of a node
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    # get the balance factor of a node
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    # Left rotation to balance the tree
    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    # Right rotation to balance the tree
    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y
    
    # Search for an order with a given order_id in the tree
    def search(self, order_id):
        return self._search(self.root, order_id)

    # Helper function to recursively search for an order in the tree
    def _search(self, node, order_id):
        if node is None:
            return None
        
        # Traverse the left subtree
        left_result = self._search(node.left, order_id)
        if left_result:
            return left_result
        
        # Check if the current node's order_id matches the input order_id
        if node.order_id == order_id:
            return node
        
        # Traverse the right subtree
        right_result = self._search(node.right, order_id)
        if right_result:
            return right_result
        
        # If no match found in the current subtree, return None
        return None

    # Find the predecessor node of a given order priority
    def find_predecessor(self, priority):
        current = self.root
        predecessor = None

        # Traverse the tree until the node with the given priority is found
        while current:
            if priority < current.priority:
                current = current.left
            elif priority > current.priority:
                predecessor = current
                current = current.right
            else:  # If we find the node with the given priority
                if current.left:
                    # The predecessor will be the maximum value in the left subtree
                    predecessor = self._find_max(current.left)
                break
        return predecessor

    # Helper function to find the maximum value in a subtree
    def _find_max(self, node):
        # Traverse to the rightmost node of the subtree
        while node.right:
            node = node.right
        return node
    
    # Find the successor node of a given order priority
    def find_successor(self, priority):
        current = self.root
        successor = None

        # Traverse the tree until the node with the given priority is found
        while current:
            if priority < current.priority:
                successor = current
                current = current.left
            elif priority > current.priority:
                current = current.right
            else:  # If we find the node with the given priority
                if current.right: 
                    # The successor will be the minimum value in the right subtree
                    successor = self._find_min(current.right)
                break 
        return successor

    # Helper function to find the minimum value in a subtree
    def _find_min(self, node):
        # Traverse to the leftmost node of the subtree
        while node.left:
            node = node.left
        return node
    
    # Delete an order with a given order_id from the tree
    def delete(self, order_id):
        # Find the node with the given order_id
        node = self.search(order_id)
        self.root = self._delete(self.root, node.priority)

    # Helper function to recursively delete a node from the tree
    def _delete(self, node, priority):
        if not node:
            return node

        # Find the node to be deleted
        if priority < node.priority:
            node.left = self._delete(node.left, priority)
        elif priority > node.priority:
            node.right = self._delete(node.right, priority)
        else:
            # Case 1: Node with no child or only one child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Case 2: Node with two children
            # Find the inorder successor (smallest node in the right subtree)
            successor = self._find_min(node.right)
            # Replace the node's value with the successor's value
            node.priority = successor.priority
            node.order_id = successor.order_id
            node.order_creation_time = successor.order_creation_time
            node.order_value = successor.order_value
            node.delivery_time = successor.delivery_time
            node.eta = successor.eta

            # Delete the successor node
            node.right = self._delete(node.right, successor.priority)

        # Update height and balance factor
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Perform rotations if needed
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node


class DeliveryNode:
    # Constructor method to initialize a DeliveryNode object
    def __init__(self, eta, order_id):
        # Initialize attributes with provided values
        self.eta = eta
        self.order_id = order_id
        self.left = None
        self.right = None
        self.height = 1

class DeliveryTree:
    # Constructor method to initialize a DeliveryTree object
    def __init__(self):
        self.root = None

    # Insert a new delivery into the tree
    def insert(self, eta, order_id):
        self.root = self._insert(self.root, eta, order_id)

    # Helper function to recursively insert a new node into the tree
    def _insert(self, node, eta, order_id):
        if not node:
            return DeliveryNode(eta, order_id)
        elif eta < node.eta:
            node.left = self._insert(node.left, eta, order_id)
        else:
            node.right = self._insert(node.right, eta, order_id)

        # Update the height of the current node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Check and perform rotations if necessary to maintain balance
        balance = self._get_balance(node)
        if balance > 1 and eta < node.left.eta:
            return self._rotate_right(node)
        if balance < -1 and eta > node.right.eta:
            return self._rotate_left(node)
        if balance > 1 and eta > node.left.eta:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and eta < node.right.eta:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # get the height of a node
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    # get the balance factor of a node
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    # Left rotation to balance the tree
    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    # Right rotation to balance the tree
    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y
    
    # Search for an order with a given order_id in the tree
    def search(self, order_id):
        return self._search(self.root, order_id)

    # Helper function to recursively search for an order in the tree
    def _search(self, node, order_id):
        if node is None:
            return None
        
        # Traverse the left subtree
        left_result = self._search(node.left, order_id)
        if left_result:
            return left_result
        
        # Check if the current node's order_id matches the input order_id
        if node.order_id == order_id:
            return node
        
        # Traverse the right subtree
        right_result = self._search(node.right, order_id)
        if right_result:
            return right_result
        
        # If no match found in the current subtree, return None
        return None

    # Helper function to find the maximum value in a subtree
    def _find_max(self, node):
        # Traverse to the rightmost node of the subtree
        while node.right:
            node = node.right
        return node

    # Helper function to find the minimum value in a subtree
    def _find_min(self, node):
        # Traverse to the leftmost node of the subtree
        while node.left:
            node = node.left
        return node
    
    # Delete an order with a given order_id from the tree
    def delete(self, order_id):
        node = self.search(order_id)
        self.root = self._delete(self.root, node.eta)

    # Helper function to recursively delete a node from the tree
    def _delete(self, node, eta):
        if not node:
            return node

        # Find the node to be deleted
        if eta < node.eta:
            node.left = self._delete(node.left, eta)
        elif eta > node.eta:
            node.right = self._delete(node.right, eta)
        else:
            # Case 1: Node with no child or only one child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Case 2: Node with two children
            # Find the inorder successor (smallest node in the right subtree)
            successor = self._find_min(node.right)
            # Replace the node's value with the successor's value
            node.eta = successor.eta
            node.order_id = successor.order_id
            # Delete the successor node
            node.right = self._delete(node.right, successor.eta)

        # Update height and balance factor
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Perform rotations if needed
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node
    
    # Search for orders within a given time range
    def search_range(self, time1, time2):
        result = []
        self._search_range_helper(self.root, time1, time2, result)
        return result

    # Helper function to recursively search for orders within a time range
    def _search_range_helper(self, node, time1, time2, result):
        if node is None:
            return

        # Check if node's eta falls within the range
        if time1 <= node.eta <= time2:
            result.append(node.order_id)

        # Recursively search in left subtree if necessary
        if node.left and time1 <= node.eta:
            self._search_range_helper(node.left, time1, time2, result)

        # Recursively search in right subtree if necessary
        if node.right and node.eta <= time2:
            self._search_range_helper(node.right, time1, time2, result)

    # Perform an inorder traversal of the tree
    def inorder_traversal(self):
        eta_array = []
        order_id_array = []
        self._inorder_traversal_helper(self.root, eta_array, order_id_array)
        return eta_array, order_id_array

    # Helper function to perform inorder traversal recursively
    def _inorder_traversal_helper(self, node, eta_array, order_id_array):
        if node is None:
            return
        
        # Recursively traverse the left subtree
        self._inorder_traversal_helper(node.left, eta_array, order_id_array)
        
        # Process the current node
        eta_array.append(node.eta)
        order_id_array.append(node.order_id)
        
        # Recursively traverse the right subtree
        self._inorder_traversal_helper(node.right, eta_array, order_id_array)


class OMS:

    current_time = 0 # Initialize currentTime as a class variable

    def __init__(self):
        # Initialize OrderTree and DeliveryTree instances
        self.order_tree = OrderTree()
        self.delivery_tree = DeliveryTree()

    def create_order(self, order_id, order_creation_time, order_value, delivery_time):
        # Renew currentTime
        OMS.current_time = order_creation_time

        # Calculate priority
        priority = self.calculate_priority(order_creation_time, order_value)

        # Insert new node with priority as key to order_tree
        self.order_tree.insert(priority, order_id, order_creation_time, order_value, delivery_time, 0)

        # Retrieve the node for the newly inserted order
        this_node = self.order_tree.search(order_id)

        # Change the order of node in order tree since the new order's successor has an ETA earlier than current time
        while this_node and self.order_tree.find_successor(this_node.priority) and self.order_tree.find_predecessor(this_node.priority) and self.order_tree.find_successor(this_node.priority).eta < OMS.current_time:
            # If this order is in delivery tree then break loop
            if self.delivery_tree.search(self.order_tree.find_successor(this_node.priority).order_id):
                break

            # Find this node's predecessor and reduce a little of its priority to change the order in tree
            delete_priority = self.order_tree.find_predecessor(this_node.priority).priority - 0.01

            # Re-insert the node with changed priority so it goes to correct position
            self.order_tree.delete(order_id)
            self.order_tree.insert(delete_priority, order_id, order_creation_time, order_value, delivery_time, 0)

            # Loop to next node
            this_node = self.order_tree.search(order_id)

        # Calculate ETA for the order
        eta = self.calculate_eta(order_id)

        # Write creation message to a text file
        with open(output_file, "a") as file:
            file.write(f"Order {order_id} has been created - ETA: {eta}\n")

        # Insert new node with data (orderId, ETA) to delivery_tree
        self.delivery_tree.insert(eta, order_id)

        # Update ETA
        self.update_eta(order_id)
        
        # Check if any orders are delivered
        self.deliver_orders(OMS.current_time)

    def prints(self, order_id):
        # Retrieve order details from the order tree based on order ID
        order_node = self.order_tree.search(order_id)
        if order_node:
            # Extract order details
            order_creation_time = order_node.order_creation_time
            order_value = order_node.order_value
            delivery_time = order_node.delivery_time
            eta = order_node.eta
            
            # Write order details to a text file
            with open(output_file, "a") as file:
                file.write(f"[{order_id}, {order_creation_time}, {order_value}, {delivery_time}, {eta}]\n")
            
        else:
            with open(output_file, "a") as file:
                file.write("There are no orders with that ID")

    def print(self, time1, time2):
        orders = []
        # Search for orders with ETA between time1 and time2 in the delivery_tree
        orders = self.delivery_tree.search_range(time1, time2)

        # Write the result to a text file
        with open(output_file, "a") as file:
            if orders:
                # Construct the formatted string
                formatted_orders = '[' + ', '.join(str(order) for order in orders) + ']\n'
                file.write(formatted_orders)  # Write the formatted string
            else:
                file.write("There are no orders in that time period\n")

    def calculate_priority(self, order_creation_time, order_value):
        # Calculate order priority based on order creation time and value
        value_weight = 0.3
        time_weight = 0.7
        normalized_order_value = order_value / 50
        return value_weight * normalized_order_value - time_weight * order_creation_time
    
    def calculate_eta(self, order_id):
        # Calculate ETA for a given order based on its attributes and successor's attributes
        node = self.order_tree.search(order_id)
        eta = node.delivery_time # add node's delivery time first
        successor = self.order_tree.find_successor(node.priority)

        if successor is None: # no successor means first node
            eta += node.order_creation_time
        else: # add successor's delivery time and eta to this node's eta
            eta += successor.delivery_time
            eta += successor.eta
        
        # Assign added eta to node's attribute
        node.eta = eta

        return eta

    def deliver_orders(self, current_time):
        # Helper function for inorder traversal
        def traverse(node):
            if node is None:
                return
            traverse(node.left)
            # Check if the order is ready for delivery
            if node.eta <= current_time:
                # If an order is delivered, add its orderId to the list
                orderId, eta = node.order_id, node.eta
                # Delete the delivered node from delivery_tree
                self.delivery_tree.delete(orderId)
                # Write delivery message to a text file
                with open(output_file, "a") as file:
                    file.write(f"Order {orderId} has been delivered at time {eta}\n")
            traverse(node.right)

        # Start traversal from the root of the delivery_tree
        traverse(self.delivery_tree.root)

    def cancel_order(self, order_id, current_system_time):
        # Renew current_time
        OMS.current_time = current_system_time

        # Search orderId in delivery_tree
        delivery_node = self.delivery_tree.search(order_id)

        # Check if the order exists and its eta is bigger than current time
        if delivery_node and delivery_node.eta > OMS.current_time:
            # Delete the order from delivery_tree
            self.delivery_tree.delete(order_id)

            # Delete the order from order_tree
            order_node = self.order_tree.search(order_id)
            successor = self.order_tree.find_successor(order_node.priority)
            self.order_tree.delete(order_id)

            # Write cancellation message to a text file
            with open(output_file, "a") as file:
                file.write(f"Order {order_id} has been canceled\n")

            # Update affected ETA since we delete node
            self.update_eta(successor.order_id)

        # If order not found or already delivered
        else:
            # Write error message to a text file
            with open(output_file, "a") as file:
                file.write(f"Cannot cancel. Order {order_id} has already been delivered\n")
        
        # Check if any orders are delivered
        self.deliver_orders(OMS.current_time)

    def update_time(self, order_id, current_system_time, new_delivery_time):
        # Renew current_time
        OMS.current_time = current_system_time

        order_node = self.order_tree.search(order_id)
        
        # Renew delivery_time
        order_node.delivery_time = new_delivery_time

        # Search orderId in delivery_tree
        delivery_node = self.delivery_tree.search(order_id)

        # Check if the order exists and its eta is bigger than current time
        if delivery_node and delivery_node.eta > OMS.current_time: 
            # Find successor of the order tree node
            successor_node = self.order_tree.find_successor(order_node.priority)
            
            # Renew all affected nodes etas 
            self.update_eta(successor_node.order_id)

        else:
            # Write error message to text file
            with open(output_file, "a") as file:
                file.write(f"Cannot update. Order {order_id} has already been delivered\n")
        
        # Deliver orders
        self.deliver_orders(OMS.current_time)

    def update_eta(self, order_id):
        affected_order_id = []  # To store affected orderIds for writing to file
        affected_eta = []
        node = self.order_tree.search(order_id)

        while node:
            # Find the predecessor of the current node
            predecessor = self.order_tree.find_predecessor(node.priority)

            if predecessor:
                # Perform calculation on predecessor's eta
                new_eta = self.calculate_eta(predecessor.order_id)

                # Add to array
                affected_order_id.append(predecessor.order_id)
                affected_eta.append(new_eta)

                # Move to the predecessor's predecessor for the next iteration
                node = predecessor
            else:
                break  # No more predecessors, exit the loop

        if len(affected_order_id) > 0:
            # Construct the output string
            output_string = "Updated ETAs: ["
            for i in range(len(affected_order_id)):
                output_string += f"{affected_order_id[i]}: {affected_eta[i]}, "
            output_string = output_string.rstrip(", ") + "]\n"  # Remove the trailing comma and space

            # Write the output string to a file
            with open(output_file, "a") as file:
                file.write(output_string)
        
        # Update ETA in delivery_tree
        for i in range(len(affected_order_id)):
            # Search for the order_id in delivery_tree
            delivery_node = self.delivery_tree.search(affected_order_id[i])

            if delivery_node:
                # Delete old node and update new node with new ETA
                self.delivery_tree.delete(affected_order_id[i])
                self.delivery_tree.insert(affected_eta[i], affected_order_id[i])
            else:
                # Handle the case where the order_id is not found in delivery_tree
                print(f"Order ID {order_id} not found in delivery_tree.")

    def get_rank_of_order(self, order_id):
        # Perform inorder traversal to collect order IDs
        _, order_id_array = self.delivery_tree.inorder_traversal()

        # Write array contents to output file 
        for i in range(len(order_id_array)):
            if order_id == order_id_array[i]:
                with open(output_file, "a") as file:
                    file.write(f"Order {order_id} will be delivered after {i} orders.\n")
                break


def process_input(input_file):
    # Read input from the specified file
    with open(input_file, 'r') as file:
        input_str = file.read()

    # Initialize an instance of the Order Management System
    oms = OMS()

    # Split input string into lines and remove leading/trailing whitespace
    input_lines = input_str.strip().split('\n')

    # Iterate over each line in the input
    for line in input_lines:
        # Split the line into operation and parameters
        tokens = line.strip().split('(')
        operation = tokens[0]
        params = tokens[1][:-1].split(',')
        
        # Execute the corresponding operation based on the parsed command
        if operation == 'createOrder':
            # Extract parameters for creating a new order
            order_id = int(params[0])
            current_system_time = int(params[1])
            order_value = int(params[2])
            delivery_time = int(params[3])
            oms.create_order(order_id, current_system_time, order_value, delivery_time)

        elif operation == 'print':
            # Determine whether to print order details or orders within a time range
            if len(params) == 1:  # If only one parameter
                order_id = int(params[0])
                oms.prints(order_id)
            elif len(params) == 2:  # If two parameters
                time1 = int(params[0])
                time2 = int(params[1])
                oms.print(time1, time2)

        elif operation == 'getRankOfOrder':
            order_id = int(params[0])
            oms.get_rank_of_order(order_id)

        elif operation == 'cancelOrder':
            order_id = int(params[0])
            current_system_time = int(params[1])
            oms.cancel_order(order_id, current_system_time)

        elif operation == 'updateTime':
            order_id = int(params[0])
            current_system_time = int(params[1])
            new_delivery_time = int(params[2])
            oms.update_time(order_id, current_system_time, new_delivery_time)

        elif operation == 'Quit':
            # Perform inorder traversal to collect order IDs
            eta_array, order_id_array = oms.delivery_tree.inorder_traversal()

            for i in range(len(order_id_array)):
                # Write delivery times to a text file
                with open(output_file, "a") as delivery_file:
                    delivery_file.write(f"Order {order_id_array[i]} will be delivered at time {eta_array[i]}\n")

            return 


def main():
    if len(sys.argv) != 2:
        print("Usage: python gatorDelivery.py <filename>")
        sys.exit(1)
    # Process input from the input file
    process_input(input_file)
    print("Output has been written to", output_file)

if __name__ == "__main__":
    main()
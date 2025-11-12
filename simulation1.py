import numpy as np
import pandas as pd
import random
import cv2
import time

class Supermarket:
    def __init__(self, floor_image, customers):
        self.floor_image = floor_image
        self.customers = customers
        self.start_time = time.time()
        self.section_visits = {'drinks': 0, 'dairy': 0, 'spices': 0, 'fruit': 0, 'checkout': 0}
        self.revenue_per_visit = {'drinks': 5, 'dairy': 4, 'spices': 2, 'fruit': 3, 'checkout': 0}
        counter_image = cv2.imread('images/counter.png')
        if counter_image is None:
            raise FileNotFoundError("counter.png not found in the directory")
        self.counter_image = cv2.resize(counter_image, (22, 22), interpolation=cv2.INTER_AREA)

    def draw(self, customers):
        self.frame = self.floor_image.copy()
        for customer in customers:
            y, x = customer.current_location
            if customer.target_section == 'checkout' and y == 555 and customer.time_counter < 150:
                counter_x = x - 35
                if counter_x >= 0 and counter_x + 22 <= self.frame.shape[1] and y + 22 <= self.frame.shape[0]:
                    self.frame[y:y+22, counter_x:counter_x+22, :] = self.counter_image
            if customer.time_counter < 150 and y + 22 <= self.frame.shape[0] and x + 22 <= self.frame.shape[1]:
                self.frame[y:y+22, x:x+22, :] = customer.image

        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_str = f"Time: {minutes:02d}:{seconds:02d}"

        visits_str = "  ".join(f"{section.capitalize()}: {count}" for section, count in self.section_visits.items())
        total_revenue = sum(count * self.revenue_per_visit[section] for section, count in self.section_visits.items())
        revenue_str = f"Revenue: ${total_revenue}"

        cv2.putText(self.frame, time_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        text_width_time, _ = cv2.getTextSize(time_str, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        cv2.putText(self.frame, visits_str, (10 + text_width_time + 20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        text_width_visits, _ = cv2.getTextSize(visits_str, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        cv2.putText(self.frame, revenue_str, (10 + text_width_time + text_width_visits + 40, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 100, 0), 2)

class Customer:
    def __init__(self, index):
        self.index = index  # Store customer index for checkout assignment
        self.prob_matrix = pd.read_csv('data_as_outcome/transition_matrix.csv')
        self.prob_matrix = self.prob_matrix.set_index(self.prob_matrix.columns)
        cart_image = cv2.imread('images/cart.png')
        if cart_image is None:
            raise FileNotFoundError("cart.png not found in the directory")
        self.image = cv2.resize(cart_image, (22, 22), interpolation=cv2.INTER_AREA)
        self.current_location = [650, random.randint(680, 880)]
        self.target_section = np.random.choice(self.prob_matrix.columns, p=self.prob_matrix.loc['entry'].values)
        self.ty, self.tx = self.get_coordinates(self.target_section)
        self.time_counter = 0
        self.has_exited = False
        self.is_waiting = False
        self.wait_frames = 0
        self.frames_per_second = 30
        self.section_counted = False

    def get_coordinates(self, target):
        if target == 'checkout':
            # Assign checkout counter based on customer index (0: x=100, 1: x=250, 2: x=400, 3: x=535)
            checkout_positions = [100, 250, 400, 535]
            tx = checkout_positions[self.index % 4]  # Cycle through the four counters
            ty = 555
        else:
            ty = random.randint(135, 435)
            if target == 'drinks': tx = random.randint(65, 175)
            elif target == 'dairy': tx = random.randint(295, 405)
            elif target == 'spices': tx = random.randint(535, 640)
            elif target == 'fruit': tx = random.randint(755, 865)
        return ty, tx

    def next_target(self, section):
        section_probs = self.prob_matrix.loc[section]
        self.target_section = np.random.choice(section_probs.index, p=section_probs.values)
        self.ty, self.tx = self.get_coordinates(self.target_section)

    def remove_add_customer(self):
        if self.time_counter < 150:
            cart_image = cv2.imread('images/cart.png')
            if cart_image is None:
                raise FileNotFoundError("cart.png not found in the directory")
            self.image = cv2.resize(cart_image, (22, 22), interpolation=cv2.INTER_AREA)
            self.image[:,:,0] = self.image[:,:,0] * 0.3
            self.image[:,:,1] = self.image[:,:,1] * 0.3
            self.image[:,:,2] = self.image[:,:,2] * 0.9
            self.time_counter += 1
        else:
            self.image = np.zeros((22, 22, 3), dtype=np.uint8) + 255
            self.has_exited = True  # Mark customer as exited

    def move_customer(self):
        if self.has_exited:
            return  # Skip movement for exited customers
        y, x = self.current_location
        if self.ty == 555:
            if y == self.ty and x == self.tx:
                if not self.section_counted and self.target_section == 'checkout':
                    simulation.section_visits['checkout'] += 1
                    self.section_counted = True
                self.remove_add_customer()
            elif y < 470:
                self.current_location[0] += 1
            elif y >= 470:
                if x == self.tx: self.current_location[0] += 1
                if x > self.tx: self.current_location[1] -= 1
                else: self.current_location[1] += 1
        elif x == self.tx and y == self.ty:
            if not self.is_waiting:
                self.is_waiting = True
                self.wait_frames = 0
                if not self.section_counted and self.target_section in simulation.section_visits:
                    simulation.section_visits[self.target_section] += 1
                    self.section_counted = True
            if self.wait_frames < self.frames_per_second:
                self.wait_frames += 1
            else:
                self.is_waiting = False
                self.wait_frames = 0
                self.section_counted = False
                self.next_target(self.target_section)
        elif x != self.tx:
            if y == 100 or y == 450:
                if self.tx > x: self.current_location[1] += 1
                else: self.current_location[1] -= 1
            elif y < 275 or y > 450:
                self.current_location[0] -= 1
            else:
                self.current_location[0] += 1
        else:
            if self.ty < y: self.current_location[0] -= 1
            else: self.current_location[0] += 1

if __name__ == '__main__':
    print("Enter number of customers allowed")
    customer_number = int(input())
    layout_image = cv2.imread('images/floor_plan1.png')
    if layout_image is None:
        raise FileNotFoundError("floor_plan1.png not found in the directory")
    customers = [Customer(i) for i in range(customer_number)]  # Pass index to each customer
    simulation = Supermarket(layout_image, customers)

    try:
        while True:
            simulation.draw(customers)
            for customer in customers:
                customer.move_customer()
            # Check if all customers have exited
            if all(customer.has_exited for customer in customers):
                print("\n=== Simulation Results ===")
                print("Section Visit Counts:")
                for section, count in simulation.section_visits.items():
                    print(f"  {section.capitalize()}: {count}")
                print("\nIndividual Revenue by Section:")
                for section, count in simulation.section_visits.items():
                    section_revenue = count * simulation.revenue_per_visit[section]
                    print(f"  {section.capitalize()}: ${section_revenue}")
                total_revenue = sum(count * simulation.revenue_per_visit[section] for section, count in simulation.section_visits.items())
                print(f"\nTotal Revenue: ${total_revenue}")
                # Find section with highest revenue (excluding checkout)
                max_revenue_section = max(
                    {k: v for k, v in simulation.section_visits.items() if k != 'checkout'},
                    key=lambda k: simulation.section_visits[k] * simulation.revenue_per_visit[k]
                )
                print(f"\n{max_revenue_section.capitalize()} replace this section close to the entry")
                print("=========================\n")
                break
            cv2.imshow('frame', simulation.frame)
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('s'), ord('q')]:
                print("\n=== Simulation Results ===")
                print("Section Visit Counts:")
                for section, count in simulation.section_visits.items():
                    print(f"  {section.capitalize()}: {count}")
                print("\nIndividual Revenue by Section:")
                for section, count in simulation.section_visits.items():
                    section_revenue = count * simulation.revenue_per_visit[section]
                    print(f"  {section.capitalize()}: ${section_revenue}")
                total_revenue = sum(count * simulation.revenue_per_visit[section] for section, count in simulation.section_visits.items())
                print(f"\nTotal Revenue: ${total_revenue}")
                # Find section with highest revenue (excluding checkout)
                max_revenue_section = max(
                    {k: v for k, v in simulation.section_visits.items() if k != 'checkout'},
                    key=lambda k: simulation.section_visits[k] * simulation.revenue_per_visit[k]
                )
                print(f"\n{max_revenue_section.capitalize()} replace this section close to the entry")
                print("=========================\n")
                break
    except KeyboardInterrupt:
        print("\n=== Simulation Results ===")
        print("Section Visit Counts:")
        for section, count in simulation.section_visits.items():
            print(f"  {section.capitalize()}: {count}")
        print("\nIndividual Revenue by Section:")
        for section, count in simulation.section_visits.items():
            section_revenue = count * simulation.revenue_per_visit[section]
            print(f"  {section.capitalize()}: ${section_revenue}")
        total_revenue = sum(count * simulation.revenue_per_visit[section] for section, count in simulation.section_visits.items())
        print(f"\nTotal Revenue: ${total_revenue}")
        # Find section with highest revenue (excluding checkout)
        max_revenue_section = max(
            {k: v for k, v in simulation.section_visits.items() if k != 'checkout'},
            key=lambda k: simulation.section_visits[k] * simulation.revenue_per_visit[k]
        )
        print(f"\n{max_revenue_section.capitalize()} replace this section close to the entry")
        print("=========================\n")
    finally:
        cv2.destroyAllWindows()
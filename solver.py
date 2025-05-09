import json, pprint

# -------- CONFIGURATION VARIBLES --------
VERSION_NUMBER = "1.1.1"
LOGGING = True              # Turn logging on or off
TARGET_ITEM = "Bozo"        # Set target item
FIRST_GUESS = "Cain's Other Eye"    # Set first guess for simulator

# -------- POPULATE ITEMS_LIST --------
ITEMS_JSON_FILE_PATH = './items.json'       # Set filepath for items.json
FIRST_GUESS_LOG_STRING = "_" + FIRST_GUESS if FIRST_GUESS else ""
GUESS_LOG_OUTPUT_FILE = "./guessCounts/guessCount" + FIRST_GUESS_LOG_STRING + ".csv"    # Set filepath for guess log

# Function to load a json into a dictionary
def json_to_dict(filename: str):
    with open(filename) as file:
        return json.load(file)


# Function to get a dictionary of all possibilities in each category
def getDictOfCategories(items_list):

    # Populate lists of options for each category
    category_lists_dict = {
        "QUALITY" : [],
        "TYPE" : [],
        "ITEM POOL" : [],
        "DESCRIPTION" : [],
        "COLORS" : [],
        "UNLOCK" : [],
        "RELEASE" : []
    }

    for item in items_list:
        for key in item.keys():
            if key == "QUALITY":
                if item[key] not in category_lists_dict["QUALITY"]:
                    category_lists_dict["QUALITY"].append(item[key])
            if key == "TYPE":
                if item[key] not in category_lists_dict["TYPE"]:
                    category_lists_dict["TYPE"].append(item[key])
            if key == "ITEM POOL":
                elements = item[key].split(",")
                for element in elements:
                    if element not in category_lists_dict["ITEM POOL"]:
                        category_lists_dict["ITEM POOL"].append(element)
            if key == "DESCRIPTION":
                elements = item[key].split(",")
                for element in elements:
                    if element not in category_lists_dict["DESCRIPTION"]:
                        category_lists_dict["DESCRIPTION"].append(element)
            if key == "COLORS":
                elements = item[key].split(",")
                for element in elements:
                    if element not in category_lists_dict["COLORS"]:
                        category_lists_dict["COLORS"].append(element)
            if key == "UNLOCK":
                if item[key] not in category_lists_dict["UNLOCK"]:
                    category_lists_dict["UNLOCK"].append(item[key])
            if key == "RELEASE":
                if item[key] not in category_lists_dict["RELEASE"]:
                    category_lists_dict["RELEASE"].append(item[key])

    for list in category_lists_dict.keys():
        category_lists_dict[list].sort()
        
    return category_lists_dict

ITEMS_LIST = json_to_dict(ITEMS_JSON_FILE_PATH)

# -------- FUNCTIONS --------

# Function to look up an item from the list by name
def lookupItem(itemName, items_list):
    res = [item for item in items_list if item['ITEM'].lower() == itemName.lower()]
    return res[0] if len(res) > 0 else False


# Function for matching items on a simple category (partial matches are NOT possible)
def simpleCategoryMatch(guessed_item, target_item, category):
    # If categories match, return True, otherwise return False
    return 1 if guessed_item[category] == target_item[category] else 0


# Function for matching items on a simple category (partial matches are possible)
def complexCategoryMatch(guessed_item, target_item, category):
    
    # Check for Color match
    categoryMatch = "None"
    guessed_category_list = guessed_item[category].split(",")
    target_category_list = target_item[category].split(",")
    
    if guessed_category_list == target_category_list:
        categoryMatch = "Full"
    else:        
        for guessed_element in guessed_category_list:
            for target_element in target_category_list:
                if guessed_element == target_element:
                    categoryMatch = "Partial"
                    break
    
    return categoryMatch


# Function to get items after a simple match
def getMatchingItemsFromSimpleMatch(guessed_item, items_list, category, match):
    matching_items_list = []
    
    for item in items_list:
        if match == 1:
            if item[category] == guessed_item[category]:
                matching_items_list.append(item);
        elif match == 0:
            if item[category] != guessed_item[category]:
                matching_items_list.append(item);
        elif match == -1:
            matching_items_list.append(item)
    
    return matching_items_list


def getMatchingItemsFromComplexMatch(guessed_item, items_list, category, match):
    guessed_item_item_pool_list = guessed_item[category].split(",")    

    remaining_items_list = items_list.copy()
    
    if match == "None":
        for item in items_list:
            item_item_pool_list = item[category].split(",")
            if any(map(lambda element: element in item_item_pool_list, guessed_item_item_pool_list)):
                remaining_items_list.remove(item)
    elif match == "Partial":
        for item in items_list:
            item_item_pool_list = item[category].split(",")
            diff = set(item_item_pool_list).difference(guessed_item_item_pool_list)
            if diff == set(item_item_pool_list):
                remaining_items_list.remove(item)
    elif match == "Full":
        for item in items_list:
            item_item_pool_list = item[category].split(",")
            if any(map(lambda element: element not in item_item_pool_list, guessed_item_item_pool_list)) or any(map(lambda element: element not in guessed_item_item_pool_list, item_item_pool_list)):
                remaining_items_list.remove(item)
    elif match == "Hidden":
        pass
    
    matching_items_list = remaining_items_list.copy()
    
    return matching_items_list


# Function to run a guess against a target item, returns list of remaining possible items
def guessItemWithTarget(guessedItemName, targetItemName, items_list):
    
    if guessedItemName == targetItemName:
        return [lookupItem(guessedItemName, items_list)]
    else:
        # Look up Guessed Item and Target Item
        guessed_item = lookupItem(guessedItemName, items_list)
        target_item = lookupItem(targetItemName, items_list)
        
        # Remove the already guessed item
        if guessed_item in items_list:
            items_list.remove(guessed_item)
        
        # Check for simple category matches
        quality_match = simpleCategoryMatch(guessed_item, target_item, "QUALITY")
        type_match = simpleCategoryMatch(guessed_item, target_item, "TYPE")
        unlock_match = simpleCategoryMatch(guessed_item, target_item, "UNLOCK")
        release_match = simpleCategoryMatch(guessed_item, target_item, "RELEASE")
        
        # Check complex category matches
        item_pool_match = complexCategoryMatch(guessed_item, target_item, "ITEM POOL")
        description_match = complexCategoryMatch(guessed_item, target_item, "DESCRIPTION")
        color_match = complexCategoryMatch(guessed_item, target_item, "COLORS")
        
        if LOGGING:
            print("QUALITY MATCH:\t\t" + str(quality_match))
            print("TYPE MATCH:\t\t" + str(type_match))
            print("UNLOCK MATCH:\t\t" + str(unlock_match))
            print("RELEASE MATCH:\t\t" + str(release_match))

            print("ITEM POOL MATCH:\t" + item_pool_match)
            print("DESCRIPTION MATCH:\t" + description_match)
            print("COLOR MATCH:\t\t" + color_match)
        
        
            print("Original size of items list:\t\t" + str(len(items_list)))
        
        # Filter by Simple Matches
        # Filter by QUALITY match
        items_list = getMatchingItemsFromSimpleMatch(guessed_item, items_list, "QUALITY", quality_match)
        if LOGGING: print("Item count after filtering QUALITY:\t" + str(len(items_list)))
        # Filter by TYPE match
        items_list = getMatchingItemsFromSimpleMatch(guessed_item, items_list, "TYPE", type_match)
        if LOGGING: print("Item count after filtering TYPE:\t" + str(len(items_list)))
        # Filter by UNLOCK match
        items_list = getMatchingItemsFromSimpleMatch(guessed_item, items_list, "UNLOCK", unlock_match)
        if LOGGING: print("Item count after filtering UNLOCK:\t" + str(len(items_list)))
        # Filter by RELEASE match
        items_list = getMatchingItemsFromSimpleMatch(guessed_item, items_list, "RELEASE", release_match)
        if LOGGING: print("Item count after filtering RELEASE:\t" + str(len(items_list)))
        
        
        # Filter by Complex Matches
        # Filter by ITEM POOL match
        items_list = getMatchingItemsFromComplexMatch(guessed_item, items_list, "ITEM POOL", item_pool_match)
        if LOGGING: print("Item count after filtering ITEM POOL:\t" + str(len(items_list)))
        # Filter by DESCRIPTION match
        items_list = getMatchingItemsFromComplexMatch(guessed_item, items_list, "DESCRIPTION", description_match)
        if LOGGING: print("Item count after filtering DESCRIPTION:\t" + str(len(items_list)))
        # Filter by COLORS match
        items_list = getMatchingItemsFromComplexMatch(guessed_item, items_list, "COLORS", color_match)
        if LOGGING: print("Item count after filtering COLORS:\t" + str(len(items_list)))
        
        return items_list


def getSimpleInput(prompt):
    gettingInput = True
    
    while gettingInput:
        text = input(prompt + " (y/n/x): ")
        if text in "ynx":
            if text == "y":
                return 1
            elif text == "n":
                return 0
            elif text == "x":
                return -1
        else:
            print("Invalid input")


def getComplexInput(prompt):
    
    complexMatchTypeMap = {
        "n": "None",
        "p": "Partial",
        "f": "Full",
        "x": "Hidden"
    }
    
    gettingInput = True
    
    while gettingInput:
        text = input(prompt + " (n/p/f/x): ")
        if text in complexMatchTypeMap.keys():
            return complexMatchTypeMap[text]
        else:
            print("Invalid input")


# Function to run a guess with no target item, takes in category match inputs, returns list of remaining possible items
def guessItemNoTarget(guessedItemName, items_list):
    
    
    # Look up Guessed Item and Target Item
    guessed_item = lookupItem(guessedItemName, items_list)
    
    # Input simple category matches
    quality_match = getSimpleInput("QUALITY match")
    type_match = getSimpleInput("TYPE match")
    unlock_match = getSimpleInput("UNLOCK match")
    release_match = getSimpleInput("RELEASE match")
    
    # Input complex category matches
    
    item_pool_match = getComplexInput("ITEM POOL match")
    description_match = getComplexInput("DESCRIPTION match")
    color_match = getComplexInput("COLORS match")
    
    # Build list of items with remaining possible categories
    matching_items_list = items_list
    
    print("Original size of items list:\t\t" + str(len(matching_items_list)))
    
    # Filter by Simple Matches
    # Filter by QUALITY match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "QUALITY", quality_match)
    print("Item count after filtering QUALITY:\t" + str(len(matching_items_list)))
    # Filter by TYPE match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "TYPE", type_match)
    print("Item count after filtering TYPE:\t" + str(len(matching_items_list)))
    # Filter by UNLOCK match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "UNLOCK", unlock_match)
    print("Item count after filtering UNLOCK:\t" + str(len(matching_items_list)))
    # Filter by RELEASE match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "RELEASE", release_match)
    print("Item count after filtering RELEASE:\t" + str(len(matching_items_list)))
    
    # Filter by Complex Matches
    # Filter by ITEM POOL match
    matching_items_list = getMatchingItemsFromComplexMatch(guessed_item, matching_items_list, "ITEM POOL", item_pool_match)
    print("Item count after filtering ITEM POOL:\t" + str(len(matching_items_list)))
    # Filter by DESCRIPTION match
    matching_items_list = getMatchingItemsFromComplexMatch(guessed_item, matching_items_list, "DESCRIPTION", description_match)
    print("Item count after filtering DESCRIPTION:\t" + str(len(matching_items_list)))
    # Filter by COLORS match
    matching_items_list = getMatchingItemsFromComplexMatch(guessed_item, matching_items_list, "COLORS", color_match)
    print("Item count after filtering COLORS:\t" + str(len(matching_items_list)))
    
    return matching_items_list

# Function to run a guessing interface against a target item
def guessingInterfaceWithTarget(target_item, items_list):

    target = lookupItem(target_item, items_list)
    print("TARGET: ")
    pprint.pprint(target)

    guessing = True

    while guessing:
        guessText = input("Enter your guess: ")
        guess = lookupItem(guessText, items_list)
        
        if guess:        
            
            print("GUESS: ")
            pprint.pprint(guess)
            
            items_list = guessItem(guess["ITEM"], target["ITEM"], items_list)
            
            print("REMAINING OPTIONS: ")
            for item in items_list:
                print(item["ITEM"])
            
            if len(items_list) == 1:
                print("SOLVED!")
                guessing = False
            elif len(items_list) == 0:
                print("You fucked up...")
                guessing = False
        else:
            print("Item not found")

# Function to run a guessing interface without a target item
def guessingInterfaceNoTarget(items_list):
    guessing = True

    while guessing:
        guessText = input("Enter your guess: ")
        guess = lookupItem(guessText, items_list)
        
        if guess:        
            
            print("GUESS: ")
            pprint.pprint(guess)
            
            items_list = guessItemNoTarget(guess["ITEM"], items_list)
            
            print("REMAINING OPTIONS: ")
            for item in items_list:
                print(item["ITEM"])
                
            if len(items_list) == 1:
                print("SOLVED!")
                guessing = False
            elif len(items_list) == 0:
                print("You fucked up...")
                guessing = False
        else:
            print("Item not found")

def getMaxValue(dict):
    highest_value = max(dict, key=dict.get)
    print(highest_value)

def popularityCounter(items_list):
    categories_dict = getDictOfCategories(items_list)
    category_count_list = []
    
    # Get a count of the most popular possibility in each category
    
    for i, category in enumerate(categories_dict):
        category_count_list.append({category: {}})
        for possibility in categories_dict[category]:
            count = 0
            for item in items_list:
                item_list = str(item[category]).split(",")
                if str(possibility) in item_list:
                    count += 1
            category_count_list[i][category][possibility] = count
            
    # Get the most popular possibility for each category
    pop_category_dict = {}
    
    for i, currCategory in enumerate(category_count_list):
        category = list(category_count_list[i].keys())[0]
        possibilities = category_count_list[i][category]
        most_popular_possibility = max(possibilities, key=possibilities.get)
        pop_category_dict[category] = [most_popular_possibility]
    
    item_popularity_dict = {}
    
    # Count the number of most popular categories matched for each item
    for item in items_list:
        popMatchCount = 0
        for category in list(pop_category_dict):
            if category != "ITEM":
                if type(item[category]) is str:
                    item_category_list = item[category].split(",")
                else:
                    item_category_list = [item[category]]
                if any(map(lambda possibility: possibility in item_category_list, pop_category_dict[category])):
                    popMatchCount += 1
        item_popularity_dict[item["ITEM"]] = popMatchCount
        
    # Get a list of all items with the most popular matches
    most_popular_matches_value = item_popularity_dict[max(item_popularity_dict, key=item_popularity_dict.get)]
    
    most_popular_matches_list = []
    
    for i, item in enumerate(item_popularity_dict):
        if item_popularity_dict[item] == most_popular_matches_value:
            most_popular_matches_list.append(item)
    
    # Return a list of the most popular matches
    return most_popular_matches_list

# Function to run a guessing interface without a target item
def guessingInterfaceNoTargetPopularMatches(items_list):
    guessing = True

    while guessing:
        print("Most popular matches:")
        print(popularityCounter(items_list))
        guessText = input("Enter your guess: ")
        guess = lookupItem(guessText, items_list)
        
        if guess:
            
            print("GUESS: ")
            pprint.pprint(guess)
            
            items_list = guessItemNoTarget(guess["ITEM"], items_list)
            
            print("REMAINING OPTIONS: ")
            for item in items_list:
                print(item["ITEM"])
                
            if len(items_list) == 1:
                print("SOLVED!")
                guessing = False
            elif len(items_list) == 0:
                print("You fucked up...")
                guessing = False
        else:
            print("Item not found")

def simulateWithTargetItem(target_item_name, items_list, first_guess_name = None):
    target_item = lookupItem(target_item_name, items_list)
    
    guessing = True
    guessing_history_string = target_item_name + ","
    guessCount = 0

    # If a first_guess is given, do a guess with that item
    if first_guess_name:
        guessCount += 1
        
        # Guess the first popular item
        guessed_item_name = first_guess_name
        if LOGGING: print("GUESSING ITEM: " + guessed_item_name)
        items_list = guessItemWithTarget(guessed_item_name, target_item_name, items_list)
        guessing_history_string += guessed_item_name + ","

        # If the target item was guessed, exit the guessing loop
        if guessed_item_name == target_item_name:
            outputList = guessing_history_string.split(",")
            outputList.insert(1, guessCount)
            if LOGGING: print(outputList)
            guessing_history_string = ",".join(map(str, outputList))
            guessing = False
        
        # Print remaingin items after guess
        if LOGGING: print("REMAINING ITEMS: ")
        if LOGGING:
            for item in items_list:
                print(item["ITEM"])
    
    # Begin guessing
    while guessing:
        guessCount += 1

        # Find the popular remaining items
        popular_items_list = popularityCounter(items_list)
        if LOGGING: print("POPULAR ITEMS: ")
        if LOGGING: print(popular_items_list)

        # Guess the first popular item
        guessed_item_name = popular_items_list[0]
        if LOGGING: print("GUESSING ITEM: " + guessed_item_name)
        items_list = guessItemWithTarget(guessed_item_name, target_item_name, items_list)
        guessing_history_string += guessed_item_name + ","

        # If the target item was guessed, exit the guessing loop
        if guessed_item_name == target_item_name:
            outputList = guessing_history_string.split(",")
            outputList.insert(1, guessCount)
            if LOGGING: print(outputList)
            guessing_history_string = ",".join(map(str, outputList))
            guessing = False
        
        # Print remaingin items after guess
        if LOGGING: print("REMAINING ITEMS: ")
        if LOGGING: 
            for item in items_list:
                print(item["ITEM"])
    
    if LOGGING: print("Solved!")
    guessing_history_string += "\n"
    return guessing_history_string

# -------- CALL FUNCTIONS HERE --------
print("Version " + VERSION_NUMBER)

# guessingInterfaceWithTarget(TARGET_ITEM, ITEMS_LIST)

# guessingInterfaceNoTarget(ITEMS_LIST)
# guessingInterfaceNoTargetPopularMatches(ITEMS_LIST)
# remaingingItems = guessItem(TARGET_ITEM,"Eye Sore", ITEMS_LIST)
# pprint.pprint(remaingingItems)
# print(len(remaingingItems))


with open(GUESS_LOG_OUTPUT_FILE, "w") as file:
    # pprint.pprint(ITEMS_LIST)
    list_of_item_names = [item["ITEM"] for item in ITEMS_LIST]
    # print(list_of_item_names)
    
    for target_item_name in list_of_item_names:
        ITEMS_LIST = json_to_dict(ITEMS_JSON_FILE_PATH)
        guessing_history = simulateWithTargetItem(target_item_name, ITEMS_LIST, FIRST_GUESS)
        if LOGGING: print(guessing_history)
        file.write(guessing_history)
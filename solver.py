import json, pprint

# -------- CONFIGURATION VARIBLES --------
# Set target item
TARGET_ITEM = "Holy Mantle"

# -------- POPULATE ITEMS_LIST --------
# Set filepath for items.json
ITEMS_JSON_FILE_PATH = './items.json'

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
    res = [item for item in items_list if item['ITEM'] == itemName]
    return res[0] if len(res) > 0 else False


# Function for matching items on a simple category (partial matches are NOT possible)
def simpleCategoryMatch(guessed_item, target_item, category):
    # If categories match, return True, otherwise return False
    return guessed_item[category] == target_item[category]


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
        if match:
            if item[category] == guessed_item[category]:
                matching_items_list.append(item);
        else:
            if item[category] != guessed_item[category]:
                matching_items_list.append(item);
    
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
    
    matching_items_list = remaining_items_list.copy()
    
    return matching_items_list


# Function to run a guess against a target item, returns list of remaining possible items
def guessItem(guessedItemName, targetItemName, items_list):
    
    # Look up Guessed Item and Target Item
    guessed_item = lookupItem(guessedItemName, items_list)
    target_item = lookupItem(targetItemName, items_list)
    
    # Check for simple category matches
    quality_match = simpleCategoryMatch(guessed_item, target_item, "QUALITY")
    type_match = simpleCategoryMatch(guessed_item, target_item, "TYPE")
    unlock_match = simpleCategoryMatch(guessed_item, target_item, "UNLOCK")
    release_match = simpleCategoryMatch(guessed_item, target_item, "RELEASE")
    
    print("QUALITY MATCH:\t\t" + str(quality_match))
    print("TYPE MATCH:\t\t" + str(type_match))
    print("UNLOCK MATCH:\t\t" + str(unlock_match))
    print("RELEASE MATCH:\t\t" + str(release_match))

    # Check complex category matches
    item_pool_match = complexCategoryMatch(guessed_item, target_item, "ITEM POOL")
    description_match = complexCategoryMatch(guessed_item, target_item, "DESCRIPTION")
    color_match = complexCategoryMatch(guessed_item, target_item, "COLORS")
    
    print("ITEM POOL MATCH:\t" + item_pool_match)
    print("DESCRIPTION MATCH:\t" + description_match)
    print("COLOR MATCH:\t\t" + color_match)
    
    # Build list of items with remaining possible categories
    
    matching_items_list = items_list
    
    print("Original size of items list:\t\t\t\t" + str(len(matching_items_list)))
    
    # Filter by Simple Matches
    # Filter by QUALITY match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "QUALITY", quality_match)
    print("Remaining item count after filtering QUALITY:\t\t" + str(len(matching_items_list)))
    # Filter by TYPE match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "TYPE", type_match)
    print("Remaining item count after filtering TYPE:\t\t" + str(len(matching_items_list)))
    # Filter by UNLOCK match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "UNLOCK", unlock_match)
    print("Remaining item count after filtering UNLOCK:\t\t" + str(len(matching_items_list)))
    # Filter by RELEASE match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "RELEASE", release_match)
    print("Remaining item count after filtering RELEASE:\t\t" + str(len(matching_items_list)))
    
    
    # Filter by Complex Matches
    # Filter by ITEM POOL match
    matching_items_list = getMatchingItemsFromComplexMatch(guessed_item, matching_items_list, "ITEM POOL", item_pool_match)
    print("Remaining item count after filtering ITEM POOL:\t\t" + str(len(matching_items_list)))
    # Filter by DESCRIPTION match
    matching_items_list = getMatchingItemsFromComplexMatch(guessed_item, matching_items_list, "DESCRIPTION", description_match)
    print("Remaining item count after filtering DESCRIPTION:\t" + str(len(matching_items_list)))
    # Filter by COLORS match
    matching_items_list = getMatchingItemsFromComplexMatch(guessed_item, matching_items_list, "COLORS", color_match)
    print("Remaining item count after filtering COLORS:\t\t" + str(len(matching_items_list)))
    
    return matching_items_list


def getSimpleInput(prompt):
    gettingInput = True
    
    while gettingInput:
        text = input(prompt + " (y/n): ")
        if text == "y" or text == "n":
            return text == "y"
        else:
            print("Invalid input")


def getComplexInput(prompt):
    
    complexMatchTypeMap = {
        "n": "None",
        "p": "Partial",
        "f": "Full"
    }
    
    gettingInput = True
    
    while gettingInput:
        text = input(prompt + " (n/p/f): ")
        if text == "n" or text == "p" or text == "f":
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
    
    print("Original size of items list:\t\t\t\t" + str(len(matching_items_list)))
    
    # Filter by Simple Matches
    # Filter by QUALITY match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "QUALITY", quality_match)
    print("Remaining item count after filtering QUALITY:\t\t" + str(len(matching_items_list)))
    # Filter by TYPE match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "TYPE", type_match)
    print("Remaining item count after filtering TYPE:\t\t" + str(len(matching_items_list)))
    # Filter by UNLOCK match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "UNLOCK", unlock_match)
    print("Remaining item count after filtering UNLOCK:\t\t" + str(len(matching_items_list)))
    # Filter by RELEASE match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "RELEASE", release_match)
    print("Remaining item count after filtering RELEASE:\t\t" + str(len(matching_items_list)))
    
    # Filter by Complex Matches
    # Filter by ITEM POOL match
    matching_items_list = getMatchingItemsFromComplexMatch(guessed_item, matching_items_list, "ITEM POOL", item_pool_match)
    print("Remaining item count after filtering ITEM POOL:\t\t" + str(len(matching_items_list)))
    # Filter by DESCRIPTION match
    matching_items_list = getMatchingItemsFromComplexMatch(guessed_item, matching_items_list, "DESCRIPTION", description_match)
    print("Remaining item count after filtering DESCRIPTION:\t" + str(len(matching_items_list)))
    # Filter by COLORS match
    matching_items_list = getMatchingItemsFromComplexMatch(guessed_item, matching_items_list, "COLORS", color_match)
    print("Remaining item count after filtering COLORS:\t\t" + str(len(matching_items_list)))
    
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


def popularityCounter(items_list):
    categories_dict = getDictOfCategories(items_list)
    category_count_list = []
    
    for i, category in enumerate(categories_dict):
        print(category)
        category_count_list.append({category: {}})
        for possibility in categories_dict[category]:
            count = 0
            for item in items_list:
                # print(item)
                item_list = str(item[category]).split(",")
                if str(possibility) in item_list:
                    count += 1
            print(str(possibility) + ": " + str(count))
            category_count_list[i][category][possibility] = count
            

    pprint.pprint(category_count_list)
    
    with open('./count.json', 'w') as f:
        json.dump( category_count_list, f)
    
    return category_count_list
    
# -------- CALL FUNCTIONS HERE --------

# guessingInterfaceWithTarget(TARGET_ITEM, ITEMS_LIST)

# guessingInterfaceNoTarget(ITEMS_LIST)

popularityCounter(ITEMS_LIST)
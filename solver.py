import json, pprint

# Set target item
TARGET_ITEM = "Holy Mantle"
GUESSED_ITEM = "Jesus Juice"

# List of Categories
CATEGORIES = ["QUALITY", "TYPE", "ITEM POOL", "DESCRIPTION", "COLORS", "UNLOCK", "RELEASE"]

# Populate items from JSON file into a dictionary
def json_to_dict(filename: str):
    with open(filename) as file:
        return json.load(file)

items_list = json_to_dict('./items.json')

# Populate lists of options for each category

category_lists_dict = {
    "quality_list" : [],
    "type_list" : [],
    "item_pool_list" : [],
    "description_list" : [],
    "colors_list" : [],
    "unlock_list" : [],
    "release_list" : []
}

for item in items_list:
    for key in item.keys():
        if key == "QUALITY":
            if item[key] not in category_lists_dict["quality_list"]:
                category_lists_dict["quality_list"].append(item[key])
        if key == "TYPE":
            if item[key] not in category_lists_dict["type_list"]:
                category_lists_dict["type_list"].append(item[key])
        if key == "ITEM POOL":
            elements = item[key].split(",")
            for element in elements:
                if element not in category_lists_dict["item_pool_list"]:
                    category_lists_dict["item_pool_list"].append(element)
        if key == "DESCRIPTION":
            elements = item[key].split(",")
            for element in elements:
                if element not in category_lists_dict["description_list"]:
                    category_lists_dict["description_list"].append(element)
        if key == "COLORS":
            elements = item[key].split(",")
            for element in elements:
                if element not in category_lists_dict["colors_list"]:
                    category_lists_dict["colors_list"].append(element)
        if key == "UNLOCK":
            if item[key] not in category_lists_dict["unlock_list"]:
                category_lists_dict["unlock_list"].append(item[key])
        if key == "RELEASE":
            if item[key] not in category_lists_dict["release_list"]:
                category_lists_dict["release_list"].append(item[key])

for list in category_lists_dict.keys():
    category_lists_dict[list].sort()
    
# Function to look up an item from the list by name
def lookupItem(itemName, items_list):
    res = [item for item in items_list if item['ITEM'] == itemName]
    return res[0]

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

# Function to run a guess against a target item, returns list of remaining possible items
def guessItem(guessedItemName, targetItemName, items_list, category_list_dict):
    
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
    
    # Filter by Simple Matches
    # Filter by QUALITY match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "QUALITY", quality_match)
    print("Remaining item count after filtering QUALITY:\t" + str(len(matching_items_list)))
    # Filter by TYPE match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "TYPE", type_match)
    print("Remaining item count after filtering TYPE:\t" + str(len(matching_items_list)))
    # Filter by UNLOCK match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "UNLOCK", unlock_match)
    print("Remaining item count after filtering UNLOCK:\t" + str(len(matching_items_list)))
    # Filter by RELEASE match
    matching_items_list = getMatchingItemsFromSimpleMatch(guessed_item, matching_items_list, "RELEASE", release_match)
    print("Remaining item count after filtering RELEASE:\t" + str(len(matching_items_list)))
    
    
    # Filter by Complex Matches
    # Filter by ITEM POOL match
    # filtered_items_list = []
    
    # guessed_item_item_pool_list = guessed_item["ITEM POOL"].split(",")
    
    # for item in matching_items_list:
        # item_item_pool_list = item["ITEM POOL"].split(",")
        # if item_pool_match == "None":
            # for element in guessed_item_item_pool_list:
                # if element in item_item_pool_list:
                    
                
    
    return matching_items_list
    
    
target = lookupItem(TARGET_ITEM, items_list)
guess = lookupItem(GUESSED_ITEM, items_list)

print("TARGET: ")
pprint.pprint(target)
print("GUESS: ")
pprint.pprint(guess)

remaining_matches_list = guessItem(guess["ITEM"], target["ITEM"], items_list, category_lists_dict)
import json
import os
import re

DEFAULT_JSON_PATH = 'json_format'

def initial_preprocess(input_text):
    """
    Preprocess the input text to remove content after 'Module:8' and ensure Module:8 is excluded from the final JSON.
    Also, remove any occurrences of 'X hours' directly during preprocessing.
    """
    # Remove all occurrences of "X hours", "7 hours", etc.
    input_text = re.sub(r'\d+\s*hours?', '', input_text)

    lines = input_text.split('\n')
    
    # Find the line that contains 'Module:8'
    module_8_start_index = None
    for i, line in enumerate(lines):
        if line.startswith('Module:8'):
            module_8_start_index = i
            break
    
    # If 'Module:8' is found, slice the lines to keep up to but not including Module:8
    if module_8_start_index is not None:
        lines = lines[:module_8_start_index]
    
    # Join the lines back into a single text block
    return '\n'.join(lines)

def process_syllabus_to_json(input_text):
    """
    Process syllabus text and convert it to a JSON format, excluding 'Module:8' and its content,
    and removing any hour values like '7 hours' directly during preprocessing.
    """
    input_text = initial_preprocess(input_text)
    
    # Extract course code and title
    course_details = input_text.splitlines()[:2]
    course_code = course_details[0] if course_details else "Unknown Code"
    course_title = course_details[1] if len(course_details) > 1 else "Unknown Title"

    # Extract modules and their content
    modules = []
    current_module = []
    for line in input_text.splitlines()[2:]:  # Start after course details
        if line.startswith("Module:"):
            if current_module:  # If a module is already being processed, save it
                modules.append(current_module)
            current_module = [line]
        elif current_module:
            current_module.append(line)
    
    if current_module:  # Add the last module
        modules.append(current_module)

    # Create a dictionary for the syllabus
    syllabus_json = {
        "course_code": course_code,
        "course_title": course_title,
        "modules": []
    }

    # Populate modules, skip 'Module:8'
    for module in modules:
        module_number = module[0]
        if module_number == "Module:8":
            continue  # Skip Module:8

        module_content = module[1:]
        module_name = module_content[0] if module_content else "Unknown Name"
        topics = module_content[1:]  # Everything after module name is considered as topics
        
        # Remove any topics that are empty or contain hours
        topics = [topic.strip() for topic in topics if topic.strip() and not re.search(r'\d+\s*hours?', topic)]
        
        # Split the topics into individual items (separate by commas, semicolons, etc.)
        split_topics = []
        for topic in topics:
            split_topics.extend([t.strip() for t in re.split(r'[;,]\s*', topic) if t.strip()])

        # Store topics as a list of strings
        syllabus_json["modules"].append({
            "module_number": module_number,
            "module_name": module_name,
            "topics": split_topics  # Store topics as a list
        })

    return syllabus_json

def save_json_to_file(json_data, file_name):
    """
    Save the JSON data to a file.
    """
    try:
        # Ensure the default JSON path exists
        if not os.path.exists(DEFAULT_JSON_PATH):
            os.makedirs(DEFAULT_JSON_PATH)

        # Save the JSON file
        with open(os.path.join(DEFAULT_JSON_PATH, file_name), 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"JSON data successfully saved to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving JSON: {e}")


# Example syllabus input
input_text = """BCSE309L
Cryptography and Network Security
L
T
P
C
3
0
0
3
Pre-requisite 
NIL
Syllabus version 
1.0 
Course Objectives 
1. To explore the concepts of basic number theory and cryptographic techniques. 
2. To impart concept of Hash and Message Authentication, Digital Signatures and authentication protocols. 
3. To reveal the basics of transport layer security, Web Security and various types of System Security. 
Course Outcomes 
On completion of this course, students should be able to:
1. To know the fundamental mathematical concepts related to security.  
2. To understand concept of various cryptographic techniques. 
3. To apprehend the authentication and integrity process of data for various applications
4. To know fundamentals of Transport layer security, web security, E-Mail Security and IP Security
Module:1
Fundamentals of Number Theory 
Finite Fields and Number Theory: Modular arithmetic, Euclidian Algorithm, Primality Testing: Fermats and Eulers theorem, Chinese Reminder theorem, Discrete Logarithms. 
Module:2
Symmetric Encryption Algorithms
Symmetric key cryptographic techniques: Introduction to Stream cipher, Block cipher: DES, AES,IDEA, Block Cipher Operation, Random Bit Generation and RC4
Module:3
Asymmetric Encryption Algorithm and Key Exchange
Asymmetric key cryptographic techniques: principles, RSA, ElGamal, Elliptic Curve cryptography, Homomorphic Encryption and Secret Sharing, Key distribution and Key exchange protocols, Diffie-Hellman Key Exchange, Man-in-the-Meddle Attack 
Module:4
Message Digest and Hash Functions 
Requirements for Hash Functions, Security of Hash Functions, Message Digest (MD5), Secure Hash Function (SHA),Birthday Attack, HMAC 
Module:5
Digital Signature and Authentication Protocols
Authentication Requirements, Authentication Functions, Message Authentication Codes, Digital Signature Authentication, Authentication Protocols, Digital Signature Standards, RSA Digital Signature, Elgamal based Digital Signature, Authentication Applications: Kerberos, X.509 Authentication Service, Public Key Infrastructure (PKI)
Module:6
Transport Layer Security and IP Security
Transport-Layer Security, Secure Socket Layer(SSL),TLS, IP Security: Overview: IP Security Architecture, Encapsulating Payload Security  
Module:7
E-mail, Web and System Security
Electronic Mail Security, Pretty Good Privacy (PGP), S/MIME, Web Security: Web Security Considerations, Secure Electronic Transaction Protocol 
Intruders, Intrusion Detection, Password Management, Firewalls: Firewall Design Principles, Trusted Systems. 
Module:8
Contemporary Issues
Total Lecture hours:
45 hours
Text Book
1. Cryptography and Network Security-Principles and Practice, 8th Edition, by Stallings William, published by Pearson, 2020
Reference Books
1. Cryptography and Network Security, 3rd Edition, by Behrouz A   Forouzan and Depdeep Mukhopadhyay, published by McGrawHill, 2015
Mode of Evaluation: CAT, written assignment, Quiz, and FAT 
Recommended by Board of Studies
04-03-2022 
Approved by Academic Council
No. 65 
Date
17-03-2022 
"""

# Process the syllabus text
syllabus_json = process_syllabus_to_json(input_text)

# Output the JSON structure to verify the result
print(json.dumps(syllabus_json, indent=4))

# Save the processed JSON to a file
save_json_to_file(syllabus_json, "syllabus.json")

import subprocess
import os


# Make sure converterX.X.jar are in the same directory as this SavegamesToXml.py
if __name__ == '__main__':
    # Parameters
    input_directory = input('path/to/directory/with/savegames: ')
    output_directory = input('path/where/you/want/xml/files/to/go: ')

    # Create a list of all file paths in the input directory, and their corresponding output path
    filepaths = list()
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            # Get input and output filepaths
            input_filepath = os.path.abspath(os.path.join(root, file))
            relative_path = os.path.relpath(input_filepath, start=input_directory)
            output_filepath = os.path.abspath(os.path.splitext(os.path.join(output_directory, relative_path))[0] + '.xml')
            filepaths.append((input_filepath, output_filepath))
            # If output directory doesn't exist, create it
            directory = os.path.dirname(output_filepath)
            if not os.path.exists(directory):
                os.makedirs(directory)

    # Run the java program to convert savegames to xml files
    for arg1, arg2 in filepaths:
        try:
            subprocess.check_output(['java', '-jar', 'converter1.9.jar', arg1, arg2])
        except subprocess.CalledProcessError:
            try:
                subprocess.check_output(['java', '-jar', 'converter2.1.jar', arg1, arg2])
            except subprocess.CalledProcessError:
                print('Version number must match either 2.1 or 1.9 (' + arg1 + ')')

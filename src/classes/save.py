import json, base64
from os import walk

from classes.scenariogenerator import ScenarioGenerator
from classes.notes import Notes

class Save:
    def write_to_file(self,name,seed,difficulty,notes):
        # Save selected seed and difficulty
        data = {'seed':seed, 'difficulty':difficulty}
        # Save the notes the player has collected
        for npc in notes:
            data[npc] = {}
            data[npc]['routine'] = notes[npc].routine
            data[npc]['company'] = notes[npc].company
            data[npc]['npc_locations'] = notes[npc].npc_location_at_time
        # Convert the data to JSON data
        json_data = json.dumps(data)
        # Using UTF-8 for seed compatibility
        data = json_data.encode("utf-8")
        # Encode the JSON string to base64 ASCII display
        content = base64.b64encode(data).decode("ascii")
        # Save the base64 ASCII data to the given file name
        file = open(f"src/data/saves/{name}.sav", "w")
        file.write(content)
        file.close()

    def load_from_file(self,name):
        # Open the given save file (may fail, change this!)
        file = open(f"src/data/saves/{name}", "r")
        # Convert file content to base64 data
        data = file.read().encode("ascii")
        # Decode base64 to JSON string
        content = base64.b64decode(data).decode("utf-8")
        # Convert JSON string to JSON data
        json_data = json.loads(content)
        # Get seed and difficulty, generate the scenario from given seed
        # and difficulty
        seed = json_data['seed']
        difficulty = json_data['difficulty']
        scenario = ScenarioGenerator(seed,difficulty)
        # Return the notes to the state they were in at the time of saving
        notes = {}
        for npc in scenario.npcs:
            note = Notes(npc,scenario)
            note.routine = json_data[npc.name]['routine']
            note.company = json_data[npc.name]['company']
            note.npc_location_at_time = json_data[npc.name]['npc_locations']
            notes[npc.name] = note
        # Return the re-generated scenario and notes
        return scenario, notes

    def list_saves(self):
        files = []
        for (dirpath, dirnames, filenames) in walk("src/data/saves"):
            files.extend(filenames)
            break
        files.remove(".gitignore")
        return files

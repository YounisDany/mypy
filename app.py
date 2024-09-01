from flask import Flask, render_template, request, jsonify
from rembg import remove
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        image_file = request.files.get('image')

        if not image_file:
            return jsonify({'error': 'No file provided'}), 400

        input_image = Image.open(image_file)
        output_image = remove(input_image)

        output_io = io.BytesIO()
        output_image.save(output_io, format='PNG')
        encoded_image = base64.b64encode(output_io.getvalue()).decode('utf-8')

        return jsonify({'image': encoded_image})

    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

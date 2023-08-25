'use client'
import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import ImageDisplay from './image_display';

interface ImageUploadProps {}

function ImageUpload(props: ImageUploadProps) {
    
    const URL_FLASK = 'http://192.168.0.7:5000/upload'
    const [message, setMessage] = useState(''); 
    const [selectedImage, setSelectedImage] = useState<string | null>(null);
    const [processedImage, setProcessedImage] = useState<string>('');

    const onDrop = async (acceptedFiles: File[]) => {
        const formData = new FormData();
        formData.append('image', acceptedFiles[0]);

        try {
        const response = await axios.post(URL_FLASK, formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            },
        });
        setMessage(response.data.message);
        setSelectedImage(URL.createObjectURL(acceptedFiles[0]));
        setProcessedImage(response.data.processed_image_url);
        } catch (error) {
        setMessage('Error al cargar la imagen');
        }
    };

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.*'],
        } // Define los tipos de archivo válidos aquí
    });

    return (
        <div>
        <h1>Cargar Imagen</h1>
        <div {...getRootProps()} className="dropzone">
            <input {...getInputProps()} />
            <p>Arrastra y suelta una imagen aquí o haz clic para seleccionar una.</p>
        </div>
        {selectedImage && (
            <div>
            <h2>Imagen Seleccionada</h2>
            <ImageDisplay imageUrl={selectedImage} altText="Imagen seleccionada" />
            </div>
        )}
        {processedImage && (
            <div>
            <h2>Imagen Procesada</h2>
            <ImageDisplay imageUrl={processedImage} altText="Imagen procesada" />
            </div>
        )}
        {message && <p>{message}</p>}
        </div>
    );
}

export default ImageUpload;

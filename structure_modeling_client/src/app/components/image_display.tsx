import React from 'react';
import Image from 'next/image'
interface ImageDisplayProps {
  imageUrl: string;
  altText: string;
}

const ImageDisplay: React.FC<ImageDisplayProps> = ({ imageUrl, altText }) => {
  
  console.log({imageUrl})
  return (
    <Image src={imageUrl} alt={altText} width={500} height={500}/>
  )
  
};

export default ImageDisplay;

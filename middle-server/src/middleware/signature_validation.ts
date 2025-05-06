import { Request, Response, NextFunction } from 'express';
import { verifySignature } from '../utils/sign';

export const validateSignature = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  const { signature, stakingKey } = req.headers;

  // Check if signature and stakingKey are present
  if (!signature || !stakingKey) {
    res.status(400).json({
      success: false,
      message: 'Signature and stakingKey are required'
    });
    return;
  }

  try {
    // Try to verify the signature of the request body
    const signatureStr = Array.isArray(signature) ? signature[0] : signature;
    const stakingKeyStr = Array.isArray(stakingKey) ? stakingKey[0] : stakingKey;
    
    const bodyStr = JSON.stringify(req.body);
    const verificationResult = await verifySignature(signatureStr, stakingKeyStr);

    if (verificationResult.error) {
      res.status(403).json({
        success: false,
        message: verificationResult.error
      });
      return;
    }

    // Optional: if you want to ensure the original payload matches the current request
    const verifiedPayload = verificationResult.data;
    if (verifiedPayload !== bodyStr) {
      res.status(403).json({
        success: false,
        message: 'Signature payload does not match request body'
      });
      return;
    }

    next();
  } catch (error) {
    console.error('Signature validation error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error during signature validation'
    });
  }
};
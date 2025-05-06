import { Request, Response, NextFunction } from 'express';
import { verifySignature } from '../utils/sign';

/**
 * Middleware to validate API request signatures
 * 
 * @description Ensures request integrity by verifying signature and payload
 * @param req Express request object
 * @param res Express response object
 * @param next Express next middleware function
 */
export const validateSignature = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  // Skip signature validation for specific routes or development environments
  if (process.env.DISABLE_SIGNATURE_VALIDATION === 'true') {
    return next();
  }

  const { signature, stakingkey } = req.headers;

  // Check if signature and stakingKey are present
  if (!signature || !stakingkey) {
    res.status(400).json({
      success: false,
      code: 'MISSING_SIGNATURE',
      message: 'Signature and stakingKey are required'
    });
    return;
  }

  try {
    const signatureStr = Array.isArray(signature) ? signature[0] : signature;
    const stakingKeyStr = Array.isArray(stakingkey) ? stakingkey[0] : stakingkey;
    
    const bodyStr = JSON.stringify(req.body);
    const verificationResult = await verifySignature(signatureStr, stakingKeyStr);

    if (verificationResult.error) {
      res.status(403).json({
        success: false,
        code: 'INVALID_SIGNATURE',
        message: verificationResult.error
      });
      return;
    }

    // Optional payload verification (can be disabled via environment variable)
    if (process.env.STRICT_PAYLOAD_VALIDATION !== 'false') {
      const verifiedPayload = verificationResult.data;
      if (verifiedPayload !== bodyStr) {
        res.status(403).json({
          success: false,
          code: 'PAYLOAD_MISMATCH',
          message: 'Signature payload does not match request body'
        });
        return;
      }
    }

    next();
  } catch (error) {
    console.error('Signature validation error:', error);
    res.status(500).json({
      success: false,
      code: 'VALIDATION_ERROR',
      message: 'Internal server error during signature validation'
    });
  }
};

/**
 * Documentation for signature generation
 * 
 * @description Provides guidelines for generating valid signatures
 * @returns Object with signature generation instructions
 */
export const getSignatureGenerationDocs = () => ({
  description: 'How to generate a valid API signature',
  steps: [
    'Stringify your request payload',
    'Use NaCl library for signing with your staking key',
    'Encode the signed message using bs58',
    'Include signature in "signature" header',
    'Include public staking key in "stakingkey" header'
  ],
  example: {
    payload: { data: 'example' },
    signingLibrary: 'tweetnacl',
    encodingMethod: 'bs58'
  }
});
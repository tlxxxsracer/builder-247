import { Request, Response, NextFunction } from 'express';
import { verifySignature } from '../utils/sign';
import { RouteValidationConfig } from './route_validator';

/**
 * Middleware for signature validation
 * Provides comprehensive signature verification with flexible configuration
 */
export async function validateSignature(
  req: Request, 
  res: Response, 
  next: NextFunction
): Promise<void> {
  // Skip validation for exempt routes or when disabled
  if (!RouteValidationConfig.shouldValidateRoute(req.path)) {
    return next();
  }

  // Environment-based validation bypass
  if (process.env.DISABLE_SIGNATURE_VALIDATION === 'true') {
    return next();
  }

  const { signature, stakingkey } = req.headers;

  // Validate signature and stakingkey presence
  if (!signature || !stakingkey) {
    res.status(400).json({
      success: false,
      code: 'SIGNATURE_MISSING',
      message: 'Signature and stakingKey are required',
      details: {
        signature: !!signature,
        stakingKey: !!stakingkey
      }
    });
    return;
  }

  try {
    // Handle potential array inputs
    const signatureStr = Array.isArray(signature) ? signature[0] : signature;
    const stakingKeyStr = Array.isArray(stakingkey) ? stakingkey[0] : stakingkey;
    
    const bodyStr = JSON.stringify(req.body);
    const verificationResult = await verifySignature(signatureStr, stakingKeyStr);

    if (verificationResult.error) {
      res.status(403).json({
        success: false,
        code: 'SIGNATURE_INVALID',
        message: verificationResult.error
      });
      return;
    }

    // Optional strict payload validation
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
}

/**
 * Generate comprehensive signature generation documentation
 * @returns Object with signature generation guidelines
 */
export function getSignatureGenerationDocs() {
  return {
    version: '1.0',
    description: 'Guidelines for generating valid API signatures',
    methods: {
      nacl: {
        library: 'tweetnacl',
        steps: [
          'Stringify request payload',
          'Use NaCl library for signing with staking key',
          'Encode signed message using bs58'
        ]
      }
    },
    headers: {
      signature: 'Base58 encoded signed payload',
      stakingkey: 'Public staking key used for verification'
    },
    example: {
      payload: { action: 'example_action' },
      signingMethod: 'NaCl detached signature'
    },
    bestPractices: [
      'Keep staking keys secure',
      'Regenerate keys periodically',
      'Use HTTPS for all API communications'
    ]
  };
}
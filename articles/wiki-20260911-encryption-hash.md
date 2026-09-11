---
title: "【Wiki】暗号化・ハッシュ処理 (Java/C# 実装リファレンス)"
emoji: "🛠️"
type: "tech"
topics: ["java", "csharp", "新人教育", "architecture", "wiki"]
published: true
---

## 1. はじめに

このWikiは、チームの技術標準として、暗号化およびハッシュ処理に関するリファレンスを提供します。特に若手エンジニアが、セキュリティ関連の処理を実装する際に「そのまま実行できる」コード例と、その背景にあるプロフェッショナルな視点を提供することを目的としています。

セキュリティはシステム開発において最も重要な側面の一つです。不適切な暗号化やハッシュ処理の実装は、情報漏洩や改ざんといった深刻なセキュリティインシデントに直結します。本ドキュメントのガイドラインとコード例に従い、安全な実装を心がけてください。

:::message
**重要**: ここに記載されたコードはあくまで基本となるリファレンスです。実際のプロダクション環境では、より堅牢なエラーハンドリング、鍵管理、設定値の外部化、そして広範なテストが不可欠です。不明な点があれば、必ずチームリーダーやセキュリティ担当者に相談してください。
:::

## 2. セキュリティの基本原則

暗号化・ハッシュ処理を行う上で共通して押さえておくべき基本原則を述べます。

### 2.1. 標準ライブラリと実績あるアルゴリズムの利用

*   **独自実装の禁止**: 独自の暗号アルゴリズムやハッシュ関数を開発することは絶対に避けてください。既知の脆弱性を含んでいる可能性が極めて高く、解読されるリスクがあります。
*   **標準ライブラリの活用**: 各言語が提供する標準の暗号ライブラリ（Java: `javax.crypto`, C#: `System.Security.Cryptography`）を優先的に使用してください。これらは専門家によって監査され、最適化されています。
*   **推奨アルゴリズムの選択**: 現在推奨されているアルゴリズム（例: AES, SHA-256/512, PBKDF2, Scrypt, Argon2, RSA, ECDSA, ECDH）を使用してください。古いアルゴリズム（例: MD5, SHA-1, DES, RC4）は、脆弱性が発見されているため使用を禁止します。

### 2.2. 鍵管理の重要性

*   暗号化の強度を決定するのは鍵の質と管理です。
*   **秘密鍵・対称鍵の保護**: 秘密鍵や対称鍵は、誰にも知られないように厳重に管理しなければなりません。ファイルシステム上の適切なアクセス制御、ハードウェアセキュリティモジュール (HSM) や鍵管理サービス (KMS) の利用を検討してください。
*   **鍵のランダム性**: 鍵は必ず暗号学的に安全な乱数生成器（後述）を使用して生成してください。
*   **鍵のローテーション**: 定期的に鍵を更新する「鍵のローテーション」を検討してください。

### 2.3. 暗号学的に安全な乱数生成器 (CSPRNG) の利用

*   鍵、IV (Initialization Vector)、ソルト、Nonce (Number used once) の生成には、必ず暗号学的に安全な乱数生成器（Java: `SecureRandom`, C#: `RandomNumberGenerator`）を使用してください。一般的な乱数生成器 (`java.util.Random`, `System.Random`) は予測可能であり、セキュリティ目的には使用できません。

### 2.4. 初期化ベクトル (IV) / ナンス (Nonce) の扱い

*   **唯一性と非予測性**: 共通鍵暗号化において、IVまたはNonceは「各暗号化操作でユニークであり、かつ予測不可能」でなければなりません。これを破ると、同じ平文が同じ暗号文になることでパターンが漏れたり、攻撃に対して脆弱になります。
*   **秘密にする必要はない**: IV/Nonce自体は秘密にする必要はなく、通常は暗号文と共に送信されます。

### 2.5. パディングと認証付き暗号

*   **パディング**: ブロック暗号では、平文の長さがブロックサイズの倍数でない場合、パディングが必要です。PKCS#5やPKCS#7が標準的です。不適切なパディングはパディングオラクル攻撃の原因となります。
*   **認証付き暗号**: 暗号化されたデータが改ざんされていないことを保証するために、認証付き暗号（Authenticated Encryption with Associated Data, AEAD）を使用してください。AES/GCMモードがこれに該当し、データ認証（MAC: Message Authentication Code）を同時に行います。CBCモードなどで別途HMACを適用することも可能ですが、GCMの方が実装が容易で安全性が高いです。

### 2.6. パスワードハッシュの要件

*   パスワードをデータベースに保存する際は、決して平文で保存せず、不可逆なハッシュ関数でハッシュ化して保存してください。
*   **ソルト (Salt)**: 各パスワードに対してユニークなソルトを生成し、パスワードと共にハッシュ化してください。ソルトがないと、レインボーテーブル攻撃や、同じパスワードを持つユーザーの判別が容易になります。
*   **ストレッチング (Stretching)**: ハッシュ計算を意図的に遅くする「ストレッチング」を行います。これにより、ブルートフォース攻撃や辞書攻撃に対する耐性を高めます。PBKDF2、Scrypt、Argon2といったキー導出関数 (KDF) がこれを提供します。

## 3. ハッシュ処理

ハッシュ関数は、任意の長さのデータから固定長のハッシュ値（ダイジェスト）を生成する一方向関数です。データの整合性チェックやパスワード保存に利用されます。

### 3.1. 共通解説

*   **用途**:
    *   **データの整合性チェック**: ファイルが改ざんされていないかを確認。
    *   **パスワード保存**: パスワードの直接保存を避け、ハッシュ値を保存。ログイン時は入力パスワードをハッシュ化して比較。
*   **推奨アルゴリズム**:
    *   **汎用ハッシュ**: SHA-256, SHA-512 (SHA-2ファミリー)
    *   **パスワードハッシュ**: PBKDF2, Scrypt, Argon2 (計算コストの高いキー導出関数)
*   **非推奨アルゴリズム**: MD5, SHA-1 (衝突攻撃に対して脆弱性が指摘されているため、使用を禁止します。)

### 3.2. Java 実装

Javaでは `java.security.MessageDigest` クラスがハッシュ計算を提供します。パスワードハッシュには `javax.crypto.SecretKeyFactory` を用いたPBKDF2を推奨します。

#### 3.2.1. SHA-256 ハッシュ

```java
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class HashExample {

    /**
     * 指定された入力文字列のSHA-256ハッシュを計算し、Base64エンコードされた文字列として返します。
     *
     * @param input ハッシュ化する文字列
     * @return Base64エンコードされたSHA-256ハッシュ文字列
     * @throws NoSuchAlgorithmException 指定されたハッシュアルゴリズムが利用できない場合
     */
    public static String calculateSha256Hash(String input) throws NoSuchAlgorithmException {
        // MessageDigestインスタンスはスレッドセーフではないため、呼び出しごとに新しいインスタンスを生成することを推奨
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hashBytes = digest.digest(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(hashBytes);
    }

    public static void main(String[] args) {
        String data = "Hello, Zenn Wiki for Encryption and Hashing!";
        try {
            String sha256Hash = calculateSha256Hash(data);
            System.out.println("Original Data: " + data);
            System.out.println("SHA-256 Hash (Base64): " + sha256Hash);

            // わずかな変更でもハッシュ値は大きく変わることを確認
            String dataModified = "Hello, Zenn Wiki for Encryption and Hashing! (modified)";
            String sha256HashModified = calculateSha256Hash(dataModified);
            System.out.println("Modified Data: " + dataModified);
            System.out.println("SHA-256 Hash (Base64): " + sha256HashModified);

        } catch (NoSuchAlgorithmException e) {
            System.err.println("Error: SHA-256 algorithm not found. " + e.getMessage());
        }
    }
}
```

#### 3.2.2. PBKDF2 によるパスワードハッシュ

パスワードハッシュには、ソルトとストレッチングを組み合わせたPBKDF2を推奨します。

```java
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.spec.InvalidKeySpecException;
import java.util.Base64;

public class PasswordHashExample {

    // 推奨されるパラメータ
    private static final int ITERATIONS = 100000; // 繰り返し回数 (計算コスト)
    private static final int KEY_LENGTH = 256;   // 鍵長 (ビット)
    private static final int SALT_LENGTH = 16;   // ソルト長 (バイト)

    /**
     * 暗号学的に安全なランダムなソルトを生成します。
     * @return ランダムなソルトのバイト配列
     */
    public static byte[] generateSalt() {
        SecureRandom random = new SecureRandom();
        byte[] salt = new byte[SALT_LENGTH];
        random.nextBytes(salt);
        return salt;
    }

    /**
     * パスワードをPBKDF2でハッシュ化します。
     *
     * @param password ハッシュ化するパスワード
     * @param saltBytes 生成されたソルトのバイト配列
     * @return Base64エンコードされたハッシュ値
     * @throws NoSuchAlgorithmException 利用可能なPBEKeySpecアルゴリズムがない場合
     * @throws InvalidKeySpecException 不正な鍵仕様の場合
     */
    public static String hashPassword(String password, byte[] saltBytes)
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), saltBytes, ITERATIONS, KEY_LENGTH);
        SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        byte[] hash = skf.generateSecret(spec).getEncoded();
        return Base64.getEncoder().encodeToString(hash);
    }

    /**
     * パスワードとハッシュ値を検証します。
     *
     * @param password 検証するパスワード
     * @param storedHash 保存されているハッシュ値 (Base64)
     * @param storedSalt 保存されているソルト (Base64)
     * @return パスワードが一致すればtrue、そうでなければfalse
     * @throws NoSuchAlgorithmException 利用可能なPBEKeySpecアルゴリズムがない場合
     * @throws InvalidKeySpecException 不正な鍵仕様の場合
     */
    public static boolean verifyPassword(String password, String storedHash, String storedSalt)
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        byte[] saltBytes = Base64.getDecoder().decode(storedSalt);
        String newHash = hashPassword(password, saltBytes);
        return newHash.equals(storedHash);
    }

    public static void main(String[] args) {
        String password = "MySuperSecretPassword123!";

        try {
            // パスワードのハッシュ化
            byte[] salt = generateSalt();
            String saltBase64 = Base64.getEncoder().encodeToString(salt);
            String hashedPassword = hashPassword(password, salt);

            System.out.println("Original Password: " + password);
            System.out.println("Generated Salt (Base64): " + saltBase64);
            System.out.println("Hashed Password (Base64): " + hashedPassword);
            System.out.println("Iterations: " + ITERATIONS + ", Key Length: " + KEY_LENGTH + ", Salt Length: " + SALT_LENGTH);

            // パスワードの検証 (正しいパスワード)
            boolean isVerified = verifyPassword(password, hashedPassword, saltBase64);
            System.out.println("Verification (Correct Password): " + isVerified);

            // パスワードの検証 (間違ったパスワード)
            boolean isVerifiedWrong = verifyPassword("WrongPassword", hashedPassword, saltBase64);
            System.out.println("Verification (Wrong Password): " + isVerifiedWrong);

        } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            System.err.println("Error during password hashing/verification: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

#### 3.2.3. プロフェッショナルな視点 (Java)

*   **`MessageDigest` のスレッドセーフティ**: `MessageDigest` インスタンスはスレッドセーフではありません。マルチスレッド環境で使用する場合は、各スレッドが独自のインスタンスを生成するか、`ThreadLocal` を使用してスレッドごとにインスタンスを管理する必要があります。
*   **パスワードハッシュの強度**:
    *   `ITERATIONS` (繰り返し回数) は、ハードウェアの進化に合わせて増やす必要があります。現在の推奨値は数万～数十万回です。ユーザーの認証遅延とのバランスも考慮してください。
    *   `KEY_LENGTH` は256ビット以上を推奨します。
    *   **より強力なアルゴリズム**: PBKDF2は広く使われていますが、メモリを大量に消費する攻撃への耐性が低いため、ScryptやArgon2の方が現代のパスワードハッシュには適しています。Javaでこれらを使用するには、Bouncy Castleなどの外部ライブラリの導入を検討してください。
*   **出力形式**: ハッシュ値はバイト配列なので、保存・転送にはBase64エンコードが一般的です。16進数文字列も使われますが、Base64の方がコンパクトです。

### 3.3. C# 実装

C#では `System.Security.Cryptography` 名前空間のクラスを使用します。ハッシュ処理には `SHA256` などのクラス、パスワードハッシュには `Rfc2898DeriveBytes` (PBKDF2) を使用します。

#### 3.3.1. SHA-256 ハッシュ

```csharp
using System;
using System.Security.Cryptography;
using System.Text;

public class HashExample
{
    /// <summary>
    /// 指定された入力文字列のSHA-256ハッシュを計算し、Base64エンコードされた文字列として返します。
    /// </summary>
    /// <param name="input">ハッシュ化する文字列</param>
    /// <returns>Base64エンコードされたSHA-256ハッシュ文字列</returns>
    public static string CalculateSha256Hash(string input)
    {
        // SHA256.Create() は推奨されるファクトリメソッド。
        // usingステートメントでIDisposableを実装するリソースを確実に解放する。
        using (SHA256 sha256 = SHA256.Create())
        {
            byte[] inputBytes = Encoding.UTF8.GetBytes(input);
            byte[] hashBytes = sha256.ComputeHash(inputBytes);
            return Convert.ToBase64String(hashBytes);
        }
    }

    public static void Main(string[] args)
    {
        string data = "Hello, Zenn Wiki for Encryption and Hashing!";
        string sha256Hash = CalculateSha256Hash(data);
        Console.WriteLine($"Original Data: {data}");
        Console.WriteLine($"SHA-256 Hash (Base64): {sha256Hash}");

        // わずかな変更でもハッシュ値は大きく変わることを確認
        string dataModified = "Hello, Zenn Wiki for Encryption and Hashing! (modified)";
        string sha256HashModified = CalculateSha256Hash(dataModified);
        Console.WriteLine($"Modified Data: {dataModified}");
        Console.WriteLine($"SHA-256 Hash (Base64): {sha256HashModified}");
    }
}
```

#### 3.3.2. PBKDF2 によるパスワードハッシュ

C#では `Rfc2898DeriveBytes` クラスがPBKDF2の実装を提供します。

```csharp
using System;
using System.Security.Cryptography;
using System.Text;

public class PasswordHashExample
{
    // 推奨されるパラメータ
    private const int ITERATIONS = 100000; // 繰り返し回数 (計算コスト)
    private const int KEY_LENGTH = 256 / 8; // 鍵長 (バイト)
    private const int SALT_LENGTH = 16;     // ソルト長 (バイト)

    /// <summary>
    /// 暗号学的に安全なランダムなソルトを生成します。
    /// </summary>
    /// <returns>ランダムなソルトのバイト配列</returns>
    public static byte[] GenerateSalt()
    {
        byte[] salt = new byte[SALT_LENGTH];
        // RandomNumberGeneratorはIDisposableを実装しているためusingを使用
        using (RandomNumberGenerator rng = RandomNumberGenerator.Create())
        {
            rng.GetBytes(salt);
        }
        return salt;
    }

    /// <summary>
    /// パスワードをPBKDF2でハッシュ化します。
    /// </summary>
    /// <param name="password">ハッシュ化するパスワード</param>
    /// <param name="saltBytes">生成されたソルトのバイト配列</param>
    /// <returns>Base64エンコードされたハッシュ値</returns>
    public static string HashPassword(string password, byte[] saltBytes)
    {
        // Rfc2898DeriveBytesはIDisposableを実装しているためusingを使用
        using (Rfc2898DeriveBytes pbkdf2 = new Rfc2898DeriveBytes(password, saltBytes, ITERATIONS, HashAlgorithmName.SHA256))
        {
            byte[] hash = pbkdf2.GetBytes(KEY_LENGTH);
            return Convert.ToBase64String(hash);
        }
    }

    /// <summary>
    /// パスワードとハッシュ値を検証します。
    /// </summary>
    /// <param name="password">検証するパスワード</param>
    /// <param name="storedHash">保存されているハッシュ値 (Base64)</param>
    /// <param name="storedSalt">保存されているソルト (Base64)</param>
    /// <returns>パスワードが一致すればtrue、そうでなければfalse</returns>
    public static bool VerifyPassword(string password, string storedHash, string storedSalt)
    {
        byte[] saltBytes = Convert.FromBase64String(storedSalt);
        string newHash = HashPassword(password, saltBytes);
        return newHash.Equals(storedHash);
    }

    public static void Main(string[] args)
    {
        string password = "MySuperSecretPassword123!";

        // パスワードのハッシュ化
        byte[] salt = GenerateSalt();
        string saltBase64 = Convert.ToBase64String(salt);
        string hashedPassword = HashPassword(password, salt);

        Console.WriteLine($"Original Password: {password}");
        Console.WriteLine($"Generated Salt (Base64): {saltBase64}");
        Console.WriteLine($"Hashed Password (Base64): {hashedPassword}");
        Console.WriteLine($"Iterations: {ITERATIONS}, Key Length: {KEY_LENGTH * 8} bits, Salt Length: {SALT_LENGTH} bytes");

        // パスワードの検証 (正しいパスワード)
        bool isVerified = VerifyPassword(password, hashedPassword, saltBase64);
        Console.WriteLine($"Verification (Correct Password): {isVerified}");

        // パスワードの検証 (間違ったパスワード)
        bool isVerifiedWrong = VerifyPassword("WrongPassword", hashedPassword, saltBase64);
        Console.WriteLine($"Verification (Wrong Password): {isVerifiedWrong}");
    }
}
```

#### 3.3.3. プロフェッショナルな視点 (C#)

*   **`using` ステートメント**: `System.Security.Cryptography` 名前空間の多くのクラスは `IDisposable` インターフェースを実装しています。`using` ステートメントを利用して、確実にリソースを解放するようにしてください。これにより、メモリリークやセキュリティ上の問題を防ぎます。
*   **`.NET Core / .NET 5+ の変更点**
    *   従来の `SHA256Managed`, `MD5CryptoServiceProvider` などは非推奨となり、`SHA256.Create()`, `MD5.Create()` のようなファクトリメソッドが推奨されます。これらはプラットフォーム固有の最適な実装を返します。
    *   `RandomNumberGenerator.Create()` が `RNGCryptoServiceProvider` の推奨される代替です。
*   **パスワードハッシュの強度**:
    *   `ITERATIONS` はJavaと同様に十分な回数を設定し、定期的に見直してください。
    *   **より強力なアルゴリズム**: .NET 5以降、`System.Security.Cryptography.Algorithms` パッケージを通じて Argon2id がサポートされるようになりました。これは現代のパスワードハッシュのベストプラクティスです。使用する際は、`Microsoft.AspNetCore.Cryptography.KeyDerivation` パッケージなども参考にしてください。
        *   例: `KeyDerivation.Pbkdf2` メソッドは `HMACSHA256` のPBKDF2を簡潔に実装できます。
        *   例: Argon2を使用する場合、別途ライブラリ (`Isopoh.Cryptography.Argon2`) の導入が必要な場合もあります。

## 4. 共通鍵暗号化 (対称鍵暗号)

共通鍵暗号は、暗号化と復号に同じ鍵を使用する方式です。高速な処理が可能で、大量のデータ暗号化に適しています。

### 4.1. 共通解説

*   **用途**: データ保存時の保護、通信経路の保護 (TLS/SSL内部で使用)。
*   **推奨アルゴリズム**: AES (Advanced Encryption Standard)。鍵長は128ビットまたは256ビットを推奨します。現在は256ビットがより安全とされています。
*   **推奨モード**: GCM (Galois/Counter Mode)。これは認証付き暗号であり、データの機密性と完全性（改ざん防止）を同時に提供します。
*   **非推奨アルゴリズム**: DES, Triple DES (3DES), RC4 (鍵長が短い、または脆弱性が発見されているため)。
*   **非推奨モード**: ECB (Electronic Codebook Mode) は、同じ平文ブロックが同じ暗号文ブロックになるため、パターンが露出し情報漏洩に繋がる可能性があります。絶対に使用しないでください。
*   **IV/Nonce**: 各暗号化処理でユニークかつ予測不可能なIV/Nonceを使用し、暗号文と共に保存・転送します。再利用は絶対に禁止です。

### 4.2. Java 実装

Javaでは `javax.crypto.Cipher` クラスを使用して共通鍵暗号化を行います。AES/GCMモードを推奨します。

```java
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;

public class AesGcmEncryptionExample {

    private static final int GCM_IV_LENGTH = 12; // GCMモードのIV/Nonce長は12バイトが推奨
    private static final int GCM_TAG_LENGTH = 16; // GCMモードの認証タグ長は16バイトが推奨 (128ビット)
    private static final String AES_ALGORITHM = "AES";
    private static final String AES_GCM_TRANSFORMATION = "AES/GCM/NoPadding"; // GCMは自身でパディング不要

    /**
     * 暗号学的に安全なAESキーを生成します。
     * @param keyLength ビット単位の鍵長 (例: 128, 256)
     * @return 生成されたSecretKey
     * @throws NoSuchAlgorithmException 指定されたアルゴリズムが利用できない場合
     */
    public static SecretKey generateAesKey(int keyLength) throws NoSuchAlgorithmException {
        KeyGenerator keyGen = KeyGenerator.getInstance(AES_ALGORITHM);
        keyGen.init(keyLength, new SecureRandom()); // SecureRandomを使用して鍵を生成
        return keyGen.generateKey();
    }

    /**
     * 暗号学的に安全なランダムなIV (Nonce) を生成します。
     * @return 生成されたIVバイト配列
     */
    public static byte[] generateIv() {
        byte[] iv = new byte[GCM_IV_LENGTH];
        new SecureRandom().nextBytes(iv);
        return iv;
    }

    /**
     * データをAES/GCMで暗号化します。
     * 暗号文にはIVと認証タグが含まれます。
     *
     * @param plaintext 暗号化する平文
     * @param secretKey AES SecretKey
     * @return Base64エンコードされたIV + 暗号文 + 認証タグの結合バイト配列
     * @throws Exception 暗号化処理中のエラー
     */
    public static String encrypt(String plaintext, SecretKey secretKey) throws Exception {
        byte[] iv = generateIv(); // 各暗号化操作で新しいIVを生成
        Cipher cipher = Cipher.getInstance(AES_GCM_TRANSFORMATION);
        GCMParameterSpec parameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH * 8, iv); // GCM_TAG_LENGTHはバイト、GCMParameterSpecはビット
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, parameterSpec);

        byte[] cipherText = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));

        // IVと暗号文、認証タグを結合して返す
        ByteBuffer byteBuffer = ByteBuffer.allocate(iv.length + cipherText.length);
        byteBuffer.put(iv);
        byteBuffer.put(cipherText); // GCMモードでは認証タグがcipherTextの末尾に含まれる
        return Base64.getEncoder().encodeToString(byteBuffer.array());
    }

    /**
     * AES/GCMで暗号化されたデータを復号します。
     *
     * @param encryptedData Base64エンコードされたIV + 暗号文 + 認証タグの結合文字列
     * @param secretKey AES SecretKey
     * @return 復号された平文
     * @throws Exception 復号処理中のエラー (認証失敗を含む)
     */
    public static String decrypt(String encryptedData, SecretKey secretKey) throws Exception {
        byte[] decodedEncryptedData = Base64.getDecoder().decode(encryptedData);

        // IVを分離
        ByteBuffer byteBuffer = ByteBuffer.wrap(decodedEncryptedData);
        byte[] iv = new byte[GCM_IV_LENGTH];
        byteBuffer.get(iv);

        // 暗号文と認証タグを分離 (GCMモードでは認証タグは暗号文の末尾にある)
        byte[] cipherTextWithTag = new byte[byteBuffer.remaining()];
        byteBuffer.get(cipherTextWithTag);

        Cipher cipher = Cipher.getInstance(AES_GCM_TRANSFORMATION);
        GCMParameterSpec parameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH * 8, iv);
        cipher.init(Cipher.DECRYPT_MODE, secretKey, parameterSpec);

        byte[] plaintext = cipher.doFinal(cipherTextWithTag); // 認証失敗時はBadPaddingExceptionがスローされる
        return new String(plaintext, StandardCharsets.UTF_8);
    }

    public static void main(String[] args) {
        try {
            // 鍵生成 (AES-256)
            SecretKey aesKey = generateAesKey(256);
            String secretKeyBase64 = Base64.getEncoder().encodeToString(aesKey.getEncoded());
            System.out.println("Generated AES Key (Base64): " + secretKeyBase64);

            String originalText = "この機密メッセージはAES/GCMで暗号化されます。Zenn Wikiはセキュリティを重視します。";
            System.out.println("Original Text: " + originalText);

            // 暗号化
            String encryptedText = encrypt(originalText, aesKey);
            System.out.println("Encrypted Text (Base64 + IV + Ciphertext + Tag): " + encryptedText);

            // 復号
            String decryptedText = decrypt(encryptedText, aesKey);
            System.out.println("Decrypted Text: " + decryptedText);

            // 鍵を再構築して検証 (本番では鍵はファイルやKMSから取得)
            byte[] keyBytes = Base64.getDecoder().decode(secretKeyBase64);
            SecretKey reconstructedKey = new SecretKeySpec(keyBytes, AES_ALGORITHM);
            String decryptedTextWithReconstructedKey = decrypt(encryptedText, reconstructedKey);
            System.out.println("Decrypted Text with reconstructed Key: " + decryptedTextWithReconstructedKey);

            // 改ざんされた暗号文の復号を試みる (認証失敗で例外発生)
            System.out.println("\n--- Tampering Test ---");
            byte[] tamperedEncryptedData = Base64.getDecoder().decode(encryptedText);
            // 適当な位置のバイトを改ざん
            if (tamperedEncryptedData.length > GCM_IV_LENGTH + 5) {
                tamperedEncryptedData[GCM_IV_LENGTH + 5] = (byte) (tamperedEncryptedData[GCM_IV_LENGTH + 5] ^ 0x01);
            }
            String tamperedEncryptedText = Base64.getEncoder().encodeToString(tamperedEncryptedData);
            try {
                decrypt(tamperedEncryptedText, aesKey);
                System.out.println("Tampering test FAILED: Decryption succeeded on tampered data.");
            } catch (Exception e) {
                System.out.println("Tampering test PASSED: Decryption failed on tampered data with error: " + e.getMessage());
            }

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

#### 4.2.1. プロフェッショナルな視点 (Java)

*   **`Cipher` インスタンスのスレッドセーフティ**: `Cipher` インスタンスはスレッドセーフではありません。`MessageDigest` と同様に、各スレッドが独自のインスタンスを生成するか、`ThreadLocal` を使用してください。
*   **GCMParameterSpec**: GCMモードでは、IVと認証タグの長さを指定する `GCMParameterSpec` が必要です。認証タグの長さ（`GCM_TAG_LENGTH * 8`）はビット単位で指定します。一般的な認証タグ長は128ビット（16バイト）です。
*   **IV (Nonce) の生成と管理**:
    *   `GCM_IV_LENGTH` は12バイトがNIST SP 800-38Dで推奨されています。これ以外の長さも許容されますが、12バイトが性能とセキュリティのバランスが良いとされています。
    *   IVは各暗号化でユニークかつ予測不可能である必要があります。`SecureRandom` で生成してください。
    *   IVは秘密にする必要はなく、暗号文と一緒に保存・転送します。
*   **認証タグ**: GCMモードでは、暗号化時に認証タグが自動的に生成され、暗号文の末尾に追加されます。復号時にこのタグが検証され、データが改ざんされていないかを確認します。認証失敗時には `AEADBadTagException` (またはその親である `BadPaddingException`) がスローされます。
*   **メモリ効率とストリーム処理**: 大量のデータを暗号化・復号する場合、`CipherInputStream` や `CipherOutputStream` を使用してストリーム処理を行うことで、メモリ効率を向上させることができます。

### 4.3. C# 実装

C#では `System.Security.Cryptography.Aes` クラスを使用して共通鍵暗号化を行います。こちらもGCMモードを推奨します。

```csharp
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

public class AesGcmEncryptionExample
{
    private const int GCM_IV_LENGTH = 12; // GCMモードのIV/Nonce長は12バイトが推奨
    private const int GCM_TAG_LENGTH = 16; // GCMモードの認証タグ長は16バイトが推奨 (128ビット)

    /// <summary>
    /// 暗号学的に安全なAESキーを生成します。
    /// </summary>
    /// <param name="keyLength">ビット単位の鍵長 (例: 128, 256)</param>
    /// <returns>生成されたSecretKeyのバイト配列</returns>
    public static byte[] GenerateAesKey(int keyLength)
    {
        using (Aes aes = Aes.Create())
        {
            aes.KeySize = keyLength;
            aes.GenerateKey();
            return aes.Key;
        }
    }

    /// <summary>
    /// 暗号学的に安全なランダムなIV (Nonce) を生成します。
    /// </summary>
    /// <returns>生成されたIVバイト配列</returns>
    public static byte[] GenerateIv()
    {
        byte[] iv = new byte[GCM_IV_LENGTH];
        using (RandomNumberGenerator rng = RandomNumberGenerator.Create())
        {
            rng.GetBytes(iv);
        }
        return iv;
    }

    /// <summary>
    /// データをAES/GCMで暗号化します。
    /// 暗号文にはIVと認証タグが含まれます。
    /// </summary>
    /// <param name="plaintext">暗号化する平文</param>
    /// <param name="keyBytes">AESキーのバイト配列</param>
    /// <returns>Base64エンコードされたIV + 暗号文 + 認証タグの結合バイト配列</returns>
    public static string Encrypt(string plaintext, byte[] keyBytes)
    {
        byte[] iv = GenerateIv(); // 各暗号化操作で新しいIVを生成
        byte[] plaintextBytes = Encoding.UTF8.GetBytes(plaintext);

        using (AesGcm aesGcm = new AesGcm(keyBytes))
        {
            byte[] cipherText = new byte[plaintextBytes.Length];
            byte[] tag = new byte[GCM_TAG_LENGTH];

            aesGcm.Encrypt(iv, plaintextBytes, cipherText, tag);

            // IV, 暗号文, タグを結合してBase64エンコード
            byte[] encryptedData = new byte[iv.Length + cipherText.Length + tag.Length];
            Buffer.BlockCopy(iv, 0, encryptedData, 0, iv.Length);
            Buffer.BlockCopy(cipherText, 0, encryptedData, iv.Length, cipherText.Length);
            Buffer.BlockCopy(tag, 0, encryptedData, iv.Length + cipherText.Length, tag.Length);

            return Convert.ToBase64String(encryptedData);
        }
    }

    /// <summary>
    /// AES/GCMで暗号化されたデータを復号します。
    /// </summary>
    /// <param name="encryptedDataString">Base64エンコードされたIV + 暗号文 + 認証タグの結合文字列</param>
    /// <param name="keyBytes">AESキーのバイト配列</param>
    /// <returns>復号された平文</returns>
    /// <exception cref="CryptographicException">認証失敗時、またはデータ形式不正時</exception>
    public static string Decrypt(string encryptedDataString, byte[] keyBytes)
    {
        byte[] encryptedData = Convert.FromBase64String(encryptedDataString);

        if (encryptedData.Length < GCM_IV_LENGTH + GCM_TAG_LENGTH)
        {
            throw new ArgumentException("Encrypted data is too short to contain IV and tag.");
        }

        // IVを分離
        byte[] iv = new byte[GCM_IV_LENGTH];
        Buffer.BlockCopy(encryptedData, 0, iv, 0, GCM_IV_LENGTH);

        // タグを分離
        byte[] tag = new byte[GCM_TAG_LENGTH];
        Buffer.BlockCopy(encryptedData, encryptedData.Length - GCM_TAG_LENGTH, tag, 0, GCM_TAG_LENGTH);

        // 暗号文を分離
        byte[] cipherText = new byte[encryptedData.Length - GCM_IV_LENGTH - GCM_TAG_LENGTH];
        Buffer.BlockCopy(encryptedData, GCM_IV_LENGTH, cipherText, 0, cipherText.Length);

        using (AesGcm aesGcm = new AesGcm(keyBytes))
        {
            byte[] decryptedBytes = new byte[cipherText.Length];
            aesGcm.Decrypt(iv, cipherText, tag, decryptedBytes); // 認証失敗時はCryptographicExceptionがスローされる
            return Encoding.UTF8.GetString(decryptedBytes);
        }
    }

    public static void Main(string[] args)
    {
        try
        {
            // 鍵生成 (AES-256)
            byte[] aesKey = GenerateAesKey(256);
            string secretKeyBase64 = Convert.ToBase64String(aesKey);
            Console.WriteLine($"Generated AES Key (Base64): {secretKeyBase64}");

            string originalText = "この機密メッセージはAES/GCMで暗号化されます。Zenn Wikiはセキュリティを重視します。";
            Console.WriteLine($"Original Text: {originalText}");

            // 暗号化
            string encryptedText = Encrypt(originalText, aesKey);
            Console.WriteLine($"Encrypted Text (Base64 + IV + Ciphertext + Tag): {encryptedText}");

            // 復号
            string decryptedText = Decrypt(encryptedText, aesKey);
            Console.WriteLine($"Decrypted Text: {decryptedText}");

            // 鍵を再構築して検証 (本番では鍵はファイルやKMSから取得)
            byte[] reconstructedKey = Convert.FromBase64String(secretKeyBase64);
            string decryptedTextWithReconstructedKey = Decrypt(encryptedText, reconstructedKey);
            Console.WriteLine($"Decrypted Text with reconstructed Key: {decryptedTextWithReconstructedKey}");


            // 改ざんされた暗号文の復号を試みる (認証失敗で例外発生)
            Console.WriteLine("\n--- Tampering Test ---");
            byte[] tamperedEncryptedData = Convert.FromBase64String(encryptedText);
            // 適当な位置のバイトを改ざん
            if (tamperedEncryptedData.Length > GCM_IV_LENGTH + 5)
            {
                tamperedEncryptedData[GCM_IV_LENGTH + 5] = (byte)(tamperedEncryptedData[GCM_IV_LENGTH + 5] ^ 0x01);
            }
            string tamperedEncryptedText = Convert.ToBase64String(tamperedEncryptedData);
            try
            {
                Decrypt(tamperedEncryptedText, aesKey);
                Console.WriteLine("Tampering test FAILED: Decryption succeeded on tampered data.");
            }
            catch (CryptographicException e)
            {
                Console.WriteLine($"Tampering test PASSED: Decryption failed on tampered data with error: {e.Message}");
            }
            catch (Exception e)
            {
                Console.WriteLine($"Tampering test PASSED (Unexpected Exception Type): Decryption failed on tampered data with error: {e.Message}");
            }
        }
        catch (Exception e)
        {
            Console.Error.WriteLine($"Error: {e.Message}");
            Console.Error.WriteLine(e.StackTrace);
        }
    }
}
```

#### 4.3.1. プロフェッショナルな視点 (C#)

*   **`AesGcm` クラス**: .NET Core 3.0以降で導入された `System.Security.Cryptography.AesGcm` クラスは、GCMモードを直接サポートし、従来の `Aes.Create()` とは異なり、より簡潔かつ安全にGCMを使用できます。従来の `Aes.Create()` で `CipherMode.GCM` を設定する場合、`ICryptoTransform` がGCMタグを内部的に処理するため、明示的なタグの分離が複雑になることがありました。`AesGcm` を使うのが推奨されます。
*   **IV (Nonce) の生成と管理**:
    *   Javaと同様に、`GCM_IV_LENGTH` は12バイトが推奨です。`RandomNumberGenerator.Create()` を使用してセキュアな乱数を生成してください。
    *   IVは暗号文と共に保存・転送します。
*   **認証タグ**: `AesGcm.Encrypt` メソッドは認証タグを別個のバイト配列として出力し、`AesGcm.Decrypt` メソッドは認証タグを引数として受け取ります。認証失敗時には `CryptographicException` がスローされます。
*   **メモリ効率とストリーム処理**: C#でも `CryptoStream` を使用してストリーム処理を行うことで、大容量データの暗号化・復号においてメモリ効率を向上させることができます。

## 5. 公開鍵暗号化 (非対称鍵暗号)

公開鍵暗号は、公開鍵と秘密鍵のペアを使用します。公開鍵で暗号化されたデータは対応する秘密鍵でのみ復号でき、秘密鍵で署名されたデータは公開鍵で検証できます。

### 5.1. 共通解説

*   **用途**:
    *   **鍵交換**: 共通鍵を安全に共有する（例: TLS/SSLハンドシェイク）
    *   **データ暗号化**: 少量データの暗号化（共通鍵は遅いため、鍵交換に使うのが一般的）
    *   **デジタル署名**: データの発信元認証と改ざん検知
*   **推奨アルゴリズム**: RSA, ECDSA (デジタル署名), ECDH (鍵交換)
*   **鍵長**:
    *   **RSA**: 2048ビット以上を推奨。3072ビットがより安全とされます。
    *   **楕円曲線暗号 (ECC)**: RSAよりも短い鍵長で同等のセキュリティ強度が得られます。
*   **パディング**:
    *   **暗号化**: OAEP (Optimal Asymmetric Encryption Padding) を推奨します。古いPKCS#1 v1.5パディングは脆弱性が見つかっています。
    *   **署名**: PSS (Probabilistic Signature Scheme) を推奨します。古いPKCS#1 v1.5署名パディングも広く使われていますが、PSSの方がより堅牢です。

### 5.2. Java 実装

Javaでは `java.security.KeyPairGenerator`, `java.security.Cipher`, `java.security.Signature` を使用して公開鍵暗号化、復号、署名、検証を行います。

```java
import javax.crypto.Cipher;
import java.security.*;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

public class RsaExample {

    private static final String RSA_ALGORITHM = "RSA";
    private static final String RSA_TRANSFORMATION_ENCRYPTION = "RSA/ECB/OAEPWithSHA-256AndMGF1Padding";
    private static final String RSA_TRANSFORMATION_SIGNATURE = "SHA256withRSA";
    private static final int RSA_KEY_SIZE = 2048; // 鍵長 (ビット)

    /**
     * RSA鍵ペアを生成します。
     * @return 生成されたKeyPair
     * @throws NoSuchAlgorithmException 指定されたアルゴリズムが利用できない場合
     */
    public static KeyPair generateRsaKeyPair() throws NoSuchAlgorithmException {
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance(RSA_ALGORITHM);
        keyPairGenerator.initialize(RSA_KEY_SIZE, new SecureRandom()); // SecureRandomで鍵を生成
        return keyPairGenerator.generateKeyPair();
    }

    /**
     * 公開鍵でデータを暗号化します。
     *
     * @param plaintext 暗号化する平文
     * @param publicKey RSA公開鍵
     * @return Base64エンコードされた暗号文
     * @throws Exception 暗号化処理中のエラー
     */
    public static String encrypt(String plaintext, PublicKey publicKey) throws Exception {
        Cipher cipher = Cipher.getInstance(RSA_TRANSFORMATION_ENCRYPTION);
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        byte[] cipherText = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(cipherText);
    }

    /**
     * 秘密鍵でデータを復号します。
     *
     * @param encryptedData Base64エンコードされた暗号文
     * @param privateKey RSA秘密鍵
     * @return 復号された平文
     * @throws Exception 復号処理中のエラー
     */
    public static String decrypt(String encryptedData, PrivateKey privateKey) throws Exception {
        byte[] decodedEncryptedData = Base64.getDecoder().decode(encryptedData);
        Cipher cipher = Cipher.getInstance(RSA_TRANSFORMATION_ENCRYPTION);
        cipher.init(Cipher.DECRYPT_MODE, privateKey);
        byte[] plaintext = cipher.doFinal(decodedEncryptedData);
        return new String(plaintext, StandardCharsets.UTF_8);
    }

    /**
     * 秘密鍵でデータにデジタル署名します。
     *
     * @param data 署名するデータ
     * @param privateKey RSA秘密鍵
     * @return Base64エンコードされた署名
     * @throws Exception 署名処理中のエラー
     */
    public static String sign(String data, PrivateKey privateKey) throws Exception {
        Signature signature = Signature.getInstance(RSA_TRANSFORMATION_SIGNATURE);
        signature.initSign(privateKey);
        signature.update(data.getBytes(StandardCharsets.UTF_8));
        byte[] signatureBytes = signature.sign();
        return Base64.getEncoder().encodeToString(signatureBytes);
    }

    /**
     * 公開鍵でデジタル署名を検証します。
     *
     * @param data 検証するデータ
     * @param signatureData Base64エンコードされた署名
     * @param publicKey RSA公開鍵
     * @return 署名が有効であればtrue、そうでなければfalse
     * @throws Exception 検証処理中のエラー
     */
    public static boolean verify(String data, String signatureData, PublicKey publicKey) throws Exception {
        byte[] decodedSignatureData = Base64.getDecoder().decode(signatureData);
        Signature signature = Signature.getInstance(RSA_TRANSFORMATION_SIGNATURE);
        signature.initVerify(publicKey);
        signature.update(data.getBytes(StandardCharsets.UTF_8));
        return signature.verify(decodedSignatureData);
    }

    /**
     * バイト配列から公開鍵を再構築します。
     */
    public static PublicKey getPublicKeyFromBytes(byte[] publicKeyBytes)
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        X509EncodedKeySpec publicKeySpec = new X509EncodedKeySpec(publicKeyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance(RSA_ALGORITHM);
        return keyFactory.generatePublic(publicKeySpec);
    }

    /**
     * バイト配列から秘密鍵を再構築します。
     */
    public static PrivateKey getPrivateKeyFromBytes(byte[] privateKeyBytes)
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        PKCS8EncodedKeySpec privateKeySpec = new PKCS8EncodedKeySpec(privateKeyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance(RSA_ALGORITHM);
        return keyFactory.generatePrivate(privateKeySpec);
    }

    public static void main(String[] args) {
        try {
            // 鍵ペア生成 (RSA-2048)
            KeyPair keyPair = generateRsaKeyPair();
            PublicKey publicKey = keyPair.getPublic();
            PrivateKey privateKey = keyPair.getPrivate();

            // 鍵のBase64エンコード表示 (本番では安全に保存)
            String publicKeyBase64 = Base64.getEncoder().encodeToString(publicKey.getEncoded());
            String privateKeyBase64 = Base64.getEncoder().encodeToString(privateKey.getEncoded());
            System.out.println("Generated Public Key (Base64): " + publicKeyBase64);
            System.out.println("Generated Private Key (Base64): " + privateKeyBase64);

            String originalMessage = "これは公開鍵暗号で守られるメッセージです。";
            System.out.println("\nOriginal Message: " + originalMessage);

            // 暗号化 (公開鍵で)
            String encryptedMessage = encrypt(originalMessage, publicKey);
            System.out.println("Encrypted Message (Base64): " + encryptedMessage);

            // 復号 (秘密鍵で)
            String decryptedMessage = decrypt(encryptedMessage, privateKey);
            System.out.println("Decrypted Message: " + decryptedMessage);

            // 署名 (秘密鍵で)
            String dataToSign = "このデータは改ざんされていませんか？";
            String signature = sign(dataToSign, privateKey);
            System.out.println("\nData to Sign: " + dataToSign);
            System.out.println("Signature (Base64): " + signature);

            // 検証 (公開鍵で)
            boolean isValidSignature = verify(dataToSign, signature, publicKey);
            System.out.println("Signature Verification (Correct data): " + isValidSignature);

            // 改ざんされたデータでの検証
            String tamperedData = "このデータは改ざんされました！";
            boolean isTamperedSignature = verify(tamperedData, signature, publicKey);
            System.out.println("Signature Verification (Tampered data): " + isTamperedSignature);

            // 鍵の再構築テスト
            PublicKey reconstructedPublicKey = getPublicKeyFromBytes(Base64.getDecoder().decode(publicKeyBase64));
            PrivateKey reconstructedPrivateKey = getPrivateKeyFromBytes(Base64.getDecoder().decode(privateKeyBase64));

            System.out.println("\nVerification with reconstructed keys:");
            System.out.println("Decrypt with reconstructed private key: " + decrypt(encryptedMessage, reconstructedPrivateKey));
            System.out.println("Verify with reconstructed public key: " + verify(dataToSign, signature, reconstructedPublicKey));


        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

#### 5.2.1. プロフェッショナルな視点 (Java)

*   **パディング方式**:
    *   暗号化には `RSA/ECB/OAEPWithSHA-256AndMGF1Padding` のようにOAEPパディングを指定してください。SHA-256とMGF1を指定することで、より堅牢になります。
    *   署名には `SHA256withRSA` のようにハッシュアルゴリズムを明示してください。Java標準ライブラリにはRSA-PSSの直接的なサポートは含まれていないため、Bouncy Castleなどの外部ライブラリを検討してください。
*   **鍵の管理**:
    *   生成された鍵ペアは、通常、ファイル（PEM/DER形式）やデータベース、KMSなどに安全に保存・ロードされます。ここでは `getEncoded()` メソッドと `KeyFactory` を使ってバイト配列からの再構築を示していますが、本番ではより堅牢な方法が必要です。
    *   特に秘密鍵は厳重に管理し、不正アクセスから保護する必要があります。
*   **暗号化できるデータサイズ**: RSAはブロック暗号であり、鍵長（例: 2048ビット = 256バイト）とパディング方式によって暗号化できる平文のサイズに上限があります。通常、数KB程度が限界です。大量のデータを暗号化する場合は、共通鍵暗号（AES）でデータを暗号化し、その共通鍵をRSAで暗号化して渡す「ハイブリッド暗号」が一般的です。

### 5.3. C# 実装

C#では `System.Security.Cryptography.RSA` クラスを使用して公開鍵暗号化、復号、署名、検証を行います。

```csharp
using System;
using System.Security.Cryptography;
using System.Text;

public class RsaExample
{
    private const int RSA_KEY_SIZE = 2048; // 鍵長 (ビット)

    /// <summary>
    /// RSA鍵ペアを生成します。
    /// </summary>
    /// <returns>生成されたRSAインスタンス (鍵ペアを含む)</returns>
    public static RSA GenerateRsaKeyPair()
    {
        RSA rsa = RSA.Create();
        rsa.KeySize = RSA_KEY_SIZE;
        return rsa;
    }

    /// <summary>
    /// 公開鍵でデータを暗号化します。
    /// </summary>
    /// <param name="plaintext">暗号化する平文</param>
    /// <param name="rsaPublicKey">RSAインスタンス (公開鍵情報を含む)</param>
    /// <returns>Base64エンコードされた暗号文</returns>
    public static string Encrypt(string plaintext, RSA rsaPublicKey)
    {
        byte[] plaintextBytes = Encoding.UTF8.GetBytes(plaintext);
        // OAEPWithSHA256パディングを推奨
        byte[] cipherText = rsaPublicKey.Encrypt(plaintextBytes, RSAEncryptionPadding.OaepSHA256);
        return Convert.ToBase64String(cipherText);
    }

    /// <summary>
    /// 秘密鍵でデータを復号します。
    /// </summary>
    /// <param name="encryptedData">Base64エンコードされた暗号文</param>
    /// <param name="rsaPrivateKey">RSAインスタンス (秘密鍵情報を含む)</param>
    /// <returns>復号された平文</returns>
    public static string Decrypt(string encryptedData, RSA rsaPrivateKey)
    {
        byte[] decodedEncryptedData = Convert.FromBase64String(encryptedData);
        // OAEPWithSHA256パディングを推奨
        byte[] plaintextBytes = rsaPrivateKey.Decrypt(decodedEncryptedData, RSAEncryptionPadding.OaepSHA256);
        return Encoding.UTF8.GetString(plaintextBytes);
    }

    /// <summary>
    /// 秘密鍵でデータにデジタル署名します。
    /// </summary>
    /// <param name="data">署名するデータ</param>
    /// <param name="rsaPrivateKey">RSAインスタンス (秘密鍵情報を含む)</param>
    /// <returns>Base64エンコードされた署名</returns>
    public static string Sign(string data, RSA rsaPrivateKey)
    {
        byte[] dataBytes = Encoding.UTF8.GetBytes(data);
        // PSS (Probabilistic Signature Scheme) を推奨
        byte[] signatureBytes = rsaPrivateKey.SignData(dataBytes, HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
        return Convert.ToBase64String(signatureBytes);
    }

    /// <summary>
    /// 公開鍵でデジタル署名を検証します。
    /// </summary>
    /// <param name="data">検証するデータ</param>
    /// <param name="signatureData">Base64エンコードされた署名</param>
    /// <param name="rsaPublicKey">RSAインスタンス (公開鍵情報を含む)</param>
    /// <returns>署名が有効であればtrue、そうでなければfalse</returns>
    public static bool Verify(string data, string signatureData, RSA rsaPublicKey)
    {
        byte[] dataBytes = Encoding.UTF8.GetBytes(data);
        byte[] decodedSignatureData = Convert.FromBase64String(signatureData);
        // PSS (Probabilistic Signature Scheme) を推奨
        return rsaPublicKey.VerifyData(dataBytes, decodedSignatureData, HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
    }

    public static void Main(string[] args)
    {
        using (RSA rsa = GenerateRsaKeyPair()) // usingでリソースを解放
        {
            // 公開鍵と秘密鍵のエクスポート/インポート
            // 公開鍵はXML、PEM、またはDER形式でエクスポート可能
            string publicKeyXml = rsa.ToXmlString(false); // false for public key only
            string privateKeyXml = rsa.ToXmlString(true); // true for private and public key

            Console.WriteLine($"Generated Public Key (XML): {publicKeyXml}");
            Console.WriteLine($"Generated Private Key (XML): {privateKeyXml}");

            string originalMessage = "これは公開鍵暗号で守られるメッセージです。";
            Console.WriteLine($"\nOriginal Message: {originalMessage}");

            // 暗号化 (公開鍵で)
            string encryptedMessage = Encrypt(originalMessage, rsa);
            Console.WriteLine($"Encrypted Message (Base64): {encryptedMessage}");

            // 復号 (秘密鍵で)
            string decryptedMessage = Decrypt(encryptedMessage, rsa);
            Console.WriteLine($"Decrypted Message: {decryptedMessage}");

            // 署名 (秘密鍵で)
            string dataToSign = "このデータは改ざんされていませんか？";
            string signature = Sign(dataToSign, rsa);
            Console.WriteLine($"\nData to Sign: {dataToSign}");
            Console.WriteLine($"Signature (Base64): {signature}");

            // 検証 (公開鍵で)
            bool isValidSignature = Verify(dataToSign, signature, rsa);
            Console.WriteLine($"Signature Verification (Correct data): {isValidSignature}");

            // 改ざんされたデータでの検証
            string tamperedData = "このデータは改ざんされました！";
            bool isTamperedSignature = Verify(tamperedData, signature, rsa);
            Console.WriteLine($"Signature Verification (Tampered data): {isTamperedSignature}");

            // 鍵の再構築テスト (XML文字列から)
            using (RSA reconstructedRsa = RSA.Create())
            {
                reconstructedRsa.FromXmlString(privateKeyXml); // 秘密鍵は公開鍵情報も含む
                Console.WriteLine("\nVerification with reconstructed keys:");
                Console.WriteLine($"Decrypt with reconstructed private key: {Decrypt(encryptedMessage, reconstructedRsa)}");
                
                // 公開鍵のみで検証する場合は、公開鍵XMLからRSAインスタンスを作成
                using (RSA reconstructedPublicKeyRsa = RSA.Create())
                {
                    reconstructedPublicKeyRsa.FromXmlString(publicKeyXml);
                    Console.WriteLine($"Verify with reconstructed public key: {Verify(dataToSign, signature, reconstructedPublicKeyRsa)}");
                }
            }
        }
        catch (Exception e)
        {
            Console.Error.WriteLine($"Error: {e.Message}");
            Console.Error.WriteLine(e.StackTrace);
        }
    }
}
```

#### 5.3.1. プロフェッショナルな視点 (C#)

*   **`RSA.Create()` と `RSACryptoServiceProvider`**:
    *   `.NET Core / .NET 5+` 以降では、`RSA.Create()` が推奨されるファクトリメソッドです。これはプラットフォーム固有の最適な実装を返します。
    *   `RSACryptoServiceProvider` はレガシーなAPIであり、使用を避けるべきです。
*   **パディング方式**:
    *   暗号化には `RSAEncryptionPadding.OaepSHA256` (OAEPパディングとSHA-256ハッシュ関数) を使用することを強く推奨します。
    *   署名には `RSASignaturePadding.Pss` (PSSパディング) を使用することを強く推奨します。古い `RSASignaturePadding.Pkcs1` も利用可能ですが、PSSの方がより堅牢です。
*   **鍵のエクスポート/インポート**:
    *   C#では `ToXmlString()` / `FromXmlString()` メソッドで鍵をXML形式でエクスポート/インポートできます。また、`ExportParameters()` / `ImportParameters()` で鍵パラメータを直接扱うことも可能です。
    *   秘密鍵を安全にファイルに保存したり、キーコンテナからロードしたりする場合には、`ExportRSAPrivateKeyPem()` や `ImportFromPem()` といったPEM形式を扱うメソッドも利用できます (Net 5+)。
    *   Javaと同様に、秘密鍵の管理は最も重要です。
*   **メモリ効率**: `RSA` クラスも `IDisposable` を実装しているので、`using` ステートメントで確実にリソースを解放してください。

## 6. 乱数生成器

鍵、IV、ソルト、Nonceといったセキュリティ関連の値を生成する際には、予測不可能な乱数を使用することが不可欠です。

### 6.1. 共通解説

*   **暗号学的に安全な乱数生成器 (CSPRNG)**: 一般的な擬似乱数生成器 (PRNG) は、シード値が分かると出力を予測できてしまうため、セキュリティ目的には絶対に使用しないでください。必ずCSPRNGを使用してください。

### 6.2. Java 実装

Javaでは `java.security.SecureRandom` クラスがCSPRNGを提供します。

```java
import java.security.SecureRandom;
import java.util.Base64;

public class SecureRandomExample {

    /**
     * 指定された長さの暗号学的に安全なランダムバイト配列を生成します。
     * @param length 生成するバイト配列の長さ
     * @return ランダムバイト配列
     */
    public static byte[] generateRandomBytes(int length) {
        SecureRandom random = new SecureRandom();
        byte[] bytes = new byte[length];
        random.nextBytes(bytes);
        return bytes;
    }

    public static void main(String[] args) {
        System.out.println("--- SecureRandom Byte Generation ---");

        // 16バイトのソルトを生成
        byte[] salt = generateRandomBytes(16);
        System.out.println("Generated 16-byte Salt (Base64): " + Base64.getEncoder().encodeToString(salt));

        // 12バイトのIV (Nonce) を生成
        byte[] iv = generateRandomBytes(12);
        System.out.println("Generated 12-byte IV (Base64): " + Base64.getEncoder().encodeToString(iv));

        // 別のソルトを生成 (予測不可能であることを確認)
        byte[] anotherSalt = generateRandomBytes(16);
        System.out.println("Generated another 16-byte Salt (Base64): " + Base64.getEncoder().encodeToString(anotherSalt));
        System.out.println("Are salts identical? " + java.util.Arrays.equals(salt, anotherSalt));
    }
}
```

### 6.3. C# 実装

C#では `System.Security.Cryptography.RandomNumberGenerator` クラスがCSPRNGを提供します。

```csharp
using System;
using System.Security.Cryptography;

public class SecureRandomExample
{
    /// <summary>
    /// 指定された長さの暗号学的に安全なランダムバイト配列を生成します。
    /// </summary>
    /// <param name="length">生成するバイト配列の長さ</param>
    /// <returns>ランダムバイト配列</returns>
    public static byte[] GenerateRandomBytes(int length)
    {
        byte[] bytes = new byte[length];
        using (RandomNumberGenerator rng = RandomNumberGenerator.Create())
        {
            rng.GetBytes(bytes);
        }
        return bytes;
    }

    public static void Main(string[] args)
    {
        Console.WriteLine("--- SecureRandom Byte Generation ---");

        // 16バイトのソルトを生成
        byte[] salt = GenerateRandomBytes(16);
        Console.WriteLine($"Generated 16-byte Salt (Base64): {Convert.ToBase64String(salt)}");

        // 12バイトのIV (Nonce) を生成
        byte[] iv = GenerateRandomBytes(12);
        Console.WriteLine($"Generated 12-byte IV (Base64): {Convert.ToBase64String(iv)}");

        // 別のソルトを生成 (予測不可能であることを確認)
        byte[] anotherSalt = GenerateRandomBytes(16);
        Console.WriteLine($"Generated another 16-byte Salt (Base64): {Convert.ToBase64String(anotherSalt)}");
        Console.WriteLine($"Are salts identical? {((ReadOnlySpan<byte>)salt).SequenceEqual(anotherSalt)}");
    }
}
```

## 7. バージョン・アップデート情報 (総合的なまとめ)

技術は常に進化しており、セキュリティ関連のプラクティスも例外ではありません。言語のバージョンアップや新しい攻撃手法の発見により、推奨される実装が変化する可能性があります。

### 7.1. Java

*   **Java 8以降**: `java.util.Base64` が標準化され、以前のApache Commons Codecなどの外部ライブラリに頼る必要がなくなりました。
*   **新しいアルゴリズムのサポート**: Javaの標準APIは堅牢ですが、新しいハッシュアルゴリズム (Scrypt, Argon2) や特定の楕円曲線アルゴリズム（EdDSAなど）には直接対応していない場合があります。これらの先進的なアルゴリズムが必要な場合は、Bouncy Castleなどの実績あるサードパーティライブラリの導入を検討してください。
*   **FIPS 140-2準拠**: 厳格なセキュリティ要件（例: 米国政府機関向け）がある場合、Java Cryptography Extension (JCE) にFIPS 140-2準拠のプロバイダ（例: Bouncy Castle FIPSプロバイダ）を追加する必要があります。

### 7.2. C# (.NET)

*   **`.NET Core` / `.NET 5+` の進化**:
    *   従来の `*CryptoServiceProvider` (`RSACryptoServiceProvider`, `RNGCryptoServiceProvider` など) はレガシーAPIとなり、`*.Create()` ファクトリメソッド（例: `RSA.Create()`, `RandomNumberGenerator.Create()`, `SHA256.Create()`）が推奨されています。これらはプラットフォーム固有の最適な実装を動的にロードします。
    *   `AesGcm` クラスが導入され、認証付き暗号の利用がより容易かつ安全になりました。
    *   Argon2idなど、より強力なパスワードハッシュアルゴリズムのサポートが進んでいます。`Microsoft.AspNetCore.Cryptography.KeyDerivation` パッケージも有用です。
*   **`using` ステートメントの重要性**: .NETの暗号関連クラスの多くは `IDisposable` を実装しています。リソースリークや潜在的なセキュリティリスクを防ぐため、常に `using` ステートメントでラップして利用してください。
*   **Span<T>の活用**: .NET Core 2.1以降で導入された `Span<T>` や `Memory<T>` は、既存のメモリ領域を効率的に扱うことで、メモリ割り当てを減らし、パフォーマンスを向上させることができます。大容量データの暗号化・復号において検討の価値があります。

## 8. その他、注意事項

*   **例外処理**: 暗号化処理は失敗する可能性のある操作（鍵が見つからない、パディングエラー、認証失敗など）を多く含みます。適切な `try-catch` ブロックを設け、セキュリティ関連の例外は詳細な情報をログに出力せず、一般的なエラーメッセージをユーザーに返すようにしてください。
*   **秘密情報のログ出力禁止**: 鍵、パスワード、平文、IV、ソルトなどの秘密情報をログファイルやコンソールに出力することは絶対に避けてください。デバッグ時も特別な注意を払い、本番環境では決して行わないでください。
*   **鍵管理戦略**: 本番環境での鍵管理は、ここでのコード例以上に重要です。鍵はアプリケーションコード内にハードコードせず、外部の安全なストレージ（KMS、HSM、セキュアな設定ファイルなど）からロードする仕組みを構築してください。
*   **定期的なセキュリティ監査とパッチ適用**: 使用しているOS、ライブラリ、ランタイムは常に最新のセキュリティパッチを適用してください。また、定期的なセキュリティ監査や脆弱性診断を計画的に実施してください。
*   **専門家との連携**: セキュリティに関する深い知識は専門的であり、常に最新情報をキャッチアップする必要があります。不明な点や、重要なセキュリティ要件の実装に際しては、必ずセキュリティ専門家やチームのリードエンジニアに相談してください。

このWikiが、チームのセキュリティ基盤を強化し、安全なシステム開発の一助となることを願います。
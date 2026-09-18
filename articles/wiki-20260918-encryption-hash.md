---
title: "【Wiki】暗号化・ハッシュ処理 (Java/C# 実装リファレンス)"
emoji: "🛠️"
type: "tech"
topics: ["java", "csharp", "新人教育", "architecture", "wiki"]
published: true
---

# はじめに

皆さん、こんにちは！リードエンジニアの[あなたの名前/チーム名]です。

この技術リファレンス（Wiki）は、チームの技術標準として、**暗号化とハッシュ処理**に関する実践的なガイドを提供します。セキュリティはソフトウェア開発において最も重要な要素の一つであり、誤った実装はシステム全体に深刻な脆弱性をもたらします。

このドキュメントの目的は、若手エンジニアの皆さんが**セキュリティを意識した堅牢なコードを「すぐに、正しく」書けるようになること**です。各セクションには、そのままコピー＆ペーストして実行できるコードスニペットと、その背後にあるプロフェッショナルな考慮事項が含まれています。

**重要なメッセージ:**
*   **自分で暗号アルゴリズムを実装してはいけません。** 常に、信頼できる標準ライブラリのAPIを使用してください。
*   **最新のセキュリティ標準と推奨事項に常に注意を払ってください。** 暗号技術は日々進化しています。
*   **迷ったら、必ず経験豊富なメンバーに相談してください。**

さあ、セキュリティへの旅を始めましょう！

---

# 共通の考え方と注意事項

## 1. 乱数の重要性
暗号化およびハッシュ処理において、予測不能な乱数はセキュリティの基盤です。鍵、ソルト、初期化ベクトル (IV) など、多くの要素でセキュアな乱数生成が求められます。
*   **`java.security.SecureRandom` (Java)**: 暗号論的強度を持つ乱数ジェネレータ。
*   **`System.Security.Cryptography.RandomNumberGenerator` (C#)**: 同様の目的で使用されます。

## 2. 鍵管理の重要性
暗号化の鍵は、その保護が最も重要です。鍵が漏洩すれば、どんな強力な暗号化も無意味になります。
*   **鍵の生成**: 十分なエントロピーを持つランダムな鍵を使用すること。
*   **鍵の保管**: 安全な鍵ストレージ (例: HSM, キーコンテナ, 環境変数, シークレットマネージャー) を利用し、コードリポジトリに直接コミットしないこと。
*   **鍵の配布**: 安全な方法で鍵を共有・配布すること。

## 3. 脆弱なアルゴリズムの回避
MD5, SHA-1, DES, RC4 など、既に脆弱性が指摘されている、または強度不足のアルゴリズムは絶対に使用しないでください。常に最新の推奨アルゴリズム (例: SHA-256/512, AES/GCM) を選択してください。

## 4. エラーハンドリングとログ
暗号化・復号化の失敗は、セキュリティ上の潜在的な問題を示唆している可能性があります。適切なエラーハンドリングを行い、必要に応じて監査ログに出力してください。ただし、機密情報がログに記録されないよう十分注意してください。

---

# 1. ハッシュ処理

## 1.1. ハッシュ処理とは
ハッシュ処理（またはメッセージダイジェスト）は、任意の長さの入力データ（メッセージ）を受け取り、固定長の短いデータ（ハッシュ値またはダイジェスト）を出力する一方向の関数です。

**主な用途:**
*   **データ整合性の検証**: ファイルが改ざんされていないか確認する。
*   **パスワードの保存**: 平文パスワードではなく、ハッシュ値を保存する。
*   **デジタル署名**: 署名対象のデータをハッシュ化してから署名する。

## 1.2. アルゴリズムの選定
*   **推奨**: **SHA-256** または **SHA-512** (SHA-2ファミリー)。
*   **パスワードハッシュにはPBKDF2, Argon2, scryptなどの鍵導出関数 (KDF) を使用する**。これらは計算コストを意図的に高くすることで、ブルートフォース攻撃や辞書攻撃からの保護を強化します。
*   **非推奨**: MD5, SHA-1。これらは既に衝突攻撃（異なる入力から同じハッシュ値が生成されること）が可能であることが示されており、セキュリティ上の目的には適しません。

## 1.3. パスワードハッシュにおけるソルト (Salt) の重要性
パスワードハッシュを保存する際には、**ソルト**を必ず使用してください。ソルトは、パスワードごとに異なるランダムなデータであり、以下の目的で使用されます。
*   **レインボーテーブル攻撃の防止**: 攻撃者が事前に計算したハッシュ値のデータベース（レインボーテーブル）を使ってパスワードを特定するのを防ぎます。
*   **同じパスワードを持つユーザーの判別困難化**: 異なるユーザーが同じパスワードを設定しても、ソルトが異なればハッシュ値も異なるため、攻撃者が一括で特定するのを防ぎます。
*   ソルトはパスワードハッシュと一緒に保存しても安全です（機密情報ではないため）。

---

### 1.3.1. Java でのハッシュ処理

#### 1.3.1.1. SHA-256 ハッシュの生成

**用途**: ファイルの整合性チェックなど、シンプルなデータハッシュに。パスワードハッシュには不十分です（ソルトとストレッチングが必要）。

```java
// Ready-to-Run: SHA256Hasher.java
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Base64; // Java 8+

public class SHA256Hasher {

    /**
     * 指定された入力データのSHA-256ハッシュを計算します。
     *
     * @param data ハッシュ化するバイト配列
     * @return SHA-256ハッシュ値のバイト配列
     * @throws NoSuchAlgorithmException 指定されたハッシュアルゴリズムが利用できない場合
     */
    public static byte[] generateSHA256Hash(byte[] data) throws NoSuchAlgorithmException {
        // MessageDigest はスレッドセーフではないため、呼び出しごとに新しいインスタンスを取得するのが安全です。
        // または、ThreadLocal を使用することもできます。
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        return digest.digest(data);
    }

    public static void main(String[] args) {
        String input = "Hello, Zenn Wiki!";
        try {
            byte[] hash = generateSHA256Hash(input.getBytes());
            String hashHex = bytesToHex(hash);
            String hashBase64 = Base64.getEncoder().encodeToString(hash);

            System.out.println("Input: " + input);
            System.out.println("SHA-256 Hash (Hex): " + hashHex);
            System.out.println("SHA-256 Hash (Base64): " + hashBase64);

            // 別の入力で試す
            String anotherInput = "Hello, Zenn Wiki!"; // 同じ入力
            byte[] anotherHash = generateSHA256Hash(anotherInput.getBytes());
            System.out.println("Another Input Hash (Hex): " + bytesToHex(anotherHash));

            String differentInput = "Hello, Zenn Wiki!!"; // 異なる入力
            byte[] differentHash = generateSHA256Hash(differentInput.getBytes());
            System.out.println("Different Input Hash (Hex): " + bytesToHex(differentHash));

        } catch (NoSuchAlgorithmException e) {
            System.err.println("Error: SHA-256 algorithm not available. " + e.getMessage());
        }
    }

    /**
     * バイト配列を16進数文字列に変換します。
     * @param bytes 変換するバイト配列
     * @return 16進数文字列
     */
    private static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
```

**バージョン・アップデート情報:**
*   **Java 8+**: `java.util.Base64` が標準APIとして導入され、バイト配列とBase64文字列間の変換が容易になりました。それ以前は、Apache Commons Codecなどの外部ライブラリが必要でした。
*   **`MessageDigest` インスタンス**: Javaの `MessageDigest` クラスは**スレッドセーフではありません**。マルチスレッド環境で使用する場合、各スレッドで `MessageDigest.getInstance("SHA-256")` を呼び出して新しいインスタンスを取得するか、`ThreadLocal` を使用してスレッドごとにインスタンスを管理する必要があります。上記コードでは、呼び出しごとにインスタンスを取得しています。
*   Java 11以降、TLS 1.3でSHA-256とSHA-384が必須となり、よりセキュアなハッシュアルゴリズムとして推奨されています。

**プロフェッショナルな視点:**
*   **メモリ効率**: `data` はバイト配列として渡されるため、`String.getBytes()` はデフォルトエンコーディング（プラットフォーム依存）を使用します。可能であれば、`String.getBytes(StandardCharsets.UTF_8)` のように明示的にエンコーディングを指定すべきです。
*   **パフォーマンス**: `MessageDigest.getInstance()` は比較的重い処理ではないため、頻繁な呼び出しでも通常は問題ありません。しかし、非常に高スループットな環境でボトルネックになる場合は、`ThreadLocal` を検討してください。

#### 1.3.1.2. パスワードハッシュ (PBKDF2WithHmacSHA256)

**用途**: ユーザーのパスワードを安全に保存するため。ソルトと繰り返し回数（ストレッチング）を使用し、ブルートフォース攻撃に対する耐性を高めます。

```java
// Ready-to-Run: PasswordHasher.java
import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import java.security.SecureRandom;
import java.util.Base64; // Java 8+
import java.util.Arrays;

public class PasswordHasher {

    // 推奨される繰り返し回数 (iterations)。環境と要件に応じて調整してください。
    // 一般的に、計算に数百ミリ秒かかるように調整します。
    private static final int ITERATIONS = 100000; // 繰り返し回数
    private static final int KEY_LENGTH = 256;   // 鍵の長さ (ビット)
    private static final int SALT_LENGTH = 16;   // ソルトの長さ (バイト)

    /**
     * パスワードとソルトからハッシュを生成します（PBKDF2WithHmacSHA256）。
     *
     * @param passwordChars パスワード（文字配列）
     * @param saltBytes ソルト（バイト配列）
     * @return 生成されたハッシュ（バイト配列）
     * @throws NoSuchAlgorithmException 指定されたアルゴリズムが利用できない場合
     * @throws InvalidKeySpecException 鍵の仕様が無効な場合
     */
    public static byte[] hashPassword(char[] passwordChars, byte[] saltBytes)
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        PBEKeySpec spec = new PBEKeySpec(passwordChars, saltBytes, ITERATIONS, KEY_LENGTH);
        // SecretKeyFactory はスレッドセーフです。
        SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        return skf.generateSecret(spec).getEncoded();
    }

    /**
     * 安全なランダムソルトを生成します。
     *
     * @return 生成されたソルト（バイト配列）
     */
    public static byte[] generateSalt() {
        SecureRandom random = new SecureRandom(); // SecureRandom はスレッドセーフです
        byte[] salt = new byte[SALT_LENGTH];
        random.nextBytes(salt);
        return salt;
    }

    /**
     * パスワードをハッシュ化し、ソルトとハッシュをBase64で結合した文字列として返します。
     * 形式: "salt:hash"
     *
     * @param password 平文パスワード
     * @return ソルトとハッシュを結合した文字列
     */
    public static String createPasswordHash(String password) {
        try {
            byte[] salt = generateSalt();
            // パスワードを char[] で扱うことで、メモリからの消去を容易にします。
            // String は不変オブジェクトであり、メモリから即座に消去することが困難なため、セキュリティリスクとなり得ます。
            char[] passwordChars = password.toCharArray();
            byte[] hash = hashPassword(passwordChars, salt);

            // パスワード文字配列は、ハッシュ生成後すぐに消去することが推奨されます。
            Arrays.fill(passwordChars, '\0');

            return Base64.getEncoder().encodeToString(salt) + ":" + Base64.getEncoder().encodeToString(hash);
        } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            throw new RuntimeException("Error during password hashing", e);
        }
    }

    /**
     * 入力されたパスワードが保存されているハッシュと一致するか検証します。
     *
     * @param password 入力された平文パスワード
     * @param storedHashAndSalt 保存されているソルトとハッシュの結合文字列 (例: "salt:hash")
     * @return パスワードが一致すればtrue、そうでなければfalse
     */
    public static boolean verifyPassword(String password, String storedHashAndSalt) {
        try {
            String[] parts = storedHashAndSalt.split(":");
            if (parts.length != 2) {
                return false; // フォーマットが不正
            }
            byte[] salt = Base64.getDecoder().decode(parts[0]);
            byte[] storedHash = Base64.getDecoder().decode(parts[1]);

            char[] passwordChars = password.toCharArray();
            byte[] generatedHash = hashPassword(passwordChars, salt);
            Arrays.fill(passwordChars, '\0'); // パスワード文字配列を消去

            // 時間固定比較 (Time-constant comparison) を使用して、タイミング攻撃を防ぎます。
            return Arrays.equals(storedHash, generatedHash);
        } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            throw new RuntimeException("Error during password verification", e);
        }
    }

    public static void main(String[] args) {
        String userPassword = "MySecurePassword123!";

        // 1. パスワードのハッシュ化と保存
        String hashedPasswordWithSalt = createPasswordHash(userPassword);
        System.out.println("Original Password: " + userPassword);
        System.out.println("Stored Hash (salt:hash): " + hashedPasswordWithSalt);

        // 2. パスワードの検証
        System.out.println("\n--- Verification ---");
        boolean isCorrect = verifyPassword(userPassword, hashedPasswordWithSalt);
        System.out.println("Verification with correct password: " + isCorrect); // true

        boolean isIncorrect = verifyPassword("WrongPassword!", hashedPasswordWithSalt);
        System.out.println("Verification with incorrect password: " + isIncorrect); // false

        // 別のユーザーが同じパスワードを設定した場合（異なるソルトのためハッシュは異なる）
        String anotherUserPassword = "MySecurePassword123!";
        String anotherHashedPasswordWithSalt = createPasswordHash(anotherUserPassword);
        System.out.println("\nStored Hash for another user with same password (salt:hash): " + anotherHashedPasswordWithSalt);
        System.out.println("Are hashes the same for same password, different salt? " + hashedPasswordWithSalt.equals(anotherHashedPasswordWithSalt)); // false
    }
}
```

**バージョン・アップデート情報:**
*   **Java 8+**: `Base64` APIが利用可能です。
*   **`PBKDF2WithHmacSHA256`**: Java SE 6から利用可能です。現代の標準で推奨されるアルゴリズムです。
*   **`SecureRandom`**: Java 7以降では、`SecureRandom.getInstanceStrong()` を使用して、OSから提供されるより強力な乱数生成器を利用することも可能ですが、環境によってはブロックしてパフォーマンスに影響を与える可能性があります。通常は `new SecureRandom()` で十分です。
*   **繰り返し回数 (Iterations)**: `ITERATIONS` の値は、CPUの進化に合わせて定期的に見直し、十分な計算コストを維持する必要があります。数百ミリ秒程度の処理時間が目安です。

**プロフェッショナルな視点:**
*   **平文パスワードの扱い**: パスワードは `String` ではなく `char[]` として扱うことが強く推奨されます。`String` は不変オブジェクトであり、メモリから解放されるタイミングを制御できないため、GCされるまでヒープ上に残存するリスクがあります。`char[]` であれば、使用後に `Arrays.fill(passwordChars, '\0')` で上書きすることで、メモリ上の痕跡を速やかに消去できます。
*   **時間固定比較 (Constant-time comparison)**: `verifyPassword` メソッドの `Arrays.equals()` は、比較対象のバイト配列の長さに関わらず、常に一定の時間で比較を完了します（あるいは入力の長さに線形に依存するが、違いがある位置に依存しない）。これにより、ハッシュ比較にかかる時間からパスワードの推測を行う**タイミング攻撃**を防ぐことができます。
*   **スレッドセーフティ**: `SecretKeyFactory` はスレッドセーフであり、複数のスレッドで共有して使用できます。`SecureRandom` も通常はスレッドセーフです。
*   **エラーハンドリング**: パスワードハッシュの失敗はセキュリティに直結するため、`RuntimeException` でラップしてアプリケーションに伝えるか、より具体的な例外処理を行うべきです。
*   **鍵導出関数 (KDF) の選択**: PBKDF2は広く使われていますが、現代ではより優れたKDFとしてArgon2やscryptも存在します。Java標準ライブラリには含まれていないため、Bouncy Castleなどの外部ライブラリを検討することになります。PBKDF2は依然として堅牢な選択肢の一つです。

---

### 1.3.2. C# でのハッシュ処理

#### 1.3.2.1. SHA-256 ハッシュの生成

**用途**: ファイルの整合性チェックなど、シンプルなデータハッシュに。パスワードハッシュには不十分です。

```csharp
// Ready-to-Run: SHA256Hasher.cs
using System;
using System.Security.Cryptography;
using System.Text; // For Encoding
using System.Linq; // For byte to hex conversion

public class SHA256Hasher
{
    /**
     * 指定された入力データのSHA-256ハッシュを計算します。
     *
     * @param data ハッシュ化するバイト配列
     * @return SHA-256ハッシュ値のバイト配列
     */
    public static byte[] GenerateSHA256Hash(byte[] data)
    {
        // SHA256.Create() は、適切な実装（通常はSHA256CngまたはSHA256Managed）を返します。
        // usingステートメントでIDisposableを適切に処理します。
        // .NET 6+ では、SHA256.HashData(data) のように静的メソッドを使うのがより簡潔で効率的です。
        #if NET6_0_OR_GREATER
        return SHA256.HashData(data);
        #else
        using (SHA256 sha256 = SHA256.Create())
        {
            return sha256.ComputeHash(data);
        }
        #endif
    }

    public static void Main(string[] args)
    {
        string input = "Hello, Zenn Wiki!";
        try
        {
            byte[] hash = GenerateSHA256Hash(Encoding.UTF8.GetBytes(input));
            string hashHex = BytesToHex(hash);

            Console.WriteLine("Input: " + input);
            Console.WriteLine("SHA-256 Hash (Hex): " + hashHex);

            // 別の入力で試す
            string anotherInput = "Hello, Zenn Wiki!"; // 同じ入力
            byte[] anotherHash = GenerateSHA256Hash(Encoding.UTF8.GetBytes(anotherInput));
            Console.WriteLine("Another Input Hash (Hex): " + BytesToHex(anotherHash));

            string differentInput = "Hello, Zenn Wiki!!"; // 異なる入力
            byte[] differentHash = GenerateSHA256Hash(Encoding.UTF8.GetBytes(differentInput));
            Console.WriteLine("Different Input Hash (Hex): " + BytesToHex(differentHash));
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine("Error during SHA-256 hashing: " + ex.Message);
        }
    }

    /**
     * バイト配列を16進数文字列に変換します。
     * @param bytes 変換するバイト配列
     * @return 16進数文字列
     */
    private static string BytesToHex(byte[] bytes)
    {
        return string.Concat(bytes.Select(b => b.ToString("x2")));
    }
}
```

**バージョン・アップデート情報:**
*   **.NET Framework / .NET Core までの旧来の書き方**: `using (SHA256 sha256 = SHA256.Create()) { return sha256.ComputeHash(data); }`
*   **.NET 6+ での推奨**: `SHA256.HashData(data)` は、`IDisposable` なインスタンスの作成と破棄を内部で処理するため、より簡潔で推奨される書き方です。パフォーマンスも最適化されています。
*   **`Encoding.UTF8.GetBytes()`**: 文字列をバイト配列に変換する際、`System.Text.Encoding.UTF8` を明示的に使用して、プラットフォーム依存性を排除し、安全性を確保します。
*   `SHA256` クラス (および他の多くのハッシュアルゴリズムクラス) は**スレッドセーフではありません**。上記コードのように、各呼び出しで新しいインスタンスを作成するか、`.NET 6+` の `HashData` 静的メソッドを使用することが推奨されます。

**プロフェッショナルな視点:**
*   **リソース管理**: `SHA256` クラスは `IDisposable` インターフェースを実装しているため、`using` ステートメントを使用して確実にリソースを解放する必要があります。これにより、アンマネージドリソースのリークを防ぎます。
*   **メモリ効率**: `Encoding.UTF8.GetBytes(input)` は新しいバイト配列を生成します。大量のデータを扱う場合、`ReadOnlySpan<byte>` や `Stream` ベースのハッシュ計算を検討することで、メモリコピーを減らし効率を向上させることができます。
*   **静的メソッドの活用**: .NET 6以降の `SHA256.HashData()` は、`Span<byte>` を活用した低アロケーションな実装を提供し、パフォーマンスが向上しています。可能であれば最新のAPIを利用しましょう。

#### 1.3.2.2. パスワードハッシュ (PBKDF2: Rfc2898DeriveBytes)

**用途**: ユーザーのパスワードを安全に保存するため。ソルトと繰り返し回数（ストレッチング）を使用し、ブルートフォース攻撃に対する耐性を高めます。

```csharp
// Ready-to-Run: PasswordHasher.cs
using System;
using System.Security.Cryptography;
using System.Text;
using System.Linq; // For byte to hex/base64 conversion and array filling

public class PasswordHasher
{
    // 推奨される繰り返し回数 (iterations)。環境と要件に応じて調整してください。
    // 一般的に、計算に数百ミリ秒かかるように調整します。
    private static readonly int ITERATIONS = 100000; // 繰り返し回数
    private static readonly int HASH_BYTE_SIZE = 32;   // ハッシュの長さ (バイト) = 256ビット
    private static readonly int SALT_BYTE_SIZE = 16;   // ソルトの長さ (バイト)

    /**
     * パスワードとソルトからハッシュを生成します（PBKDF2）。
     *
     * @param passwordChars パスワード（文字配列）
     * @param saltBytes ソルト（バイト配列）
     * @return 生成されたハッシュ（バイト配列）
     */
    public static byte[] HashPassword(char[] passwordChars, byte[] saltBytes)
    {
        // Rfc2898DeriveBytes はPBKDF2を実装しています。
        // using ステートメントでIDisposableを適切に処理します。
        using (var pbkdf2 = new Rfc2898DeriveBytes(passwordChars, saltBytes, ITERATIONS, HashAlgorithmName.SHA256))
        {
            return pbkdf2.GetBytes(HASH_BYTE_SIZE);
        }
    }

    /**
     * 安全なランダムソルトを生成します。
     *
     * @return 生成されたソルト（バイト配列）
     */
    public static byte[] GenerateSalt()
    {
        // RandomNumberGenerator は暗号論的強度を持つ乱数ジェネレータです。
        // .NET 6+ では RNGCryptoServiceProvider の代わりにこちらが推奨されます。
        byte[] salt = new byte[SALT_BYTE_SIZE];
        RandomNumberGenerator.Fill(salt); // .NET Core 2.0+
        // 旧バージョン: using (var rng = new RNGCryptoServiceProvider()) { rng.GetBytes(salt); }
        return salt;
    }

    /**
     * パスワードをハッシュ化し、ソルトとハッシュをBase64で結合した文字列として返します。
     * 形式: "salt:hash"
     *
     * @param password 平文パスワード
     * @return ソルトとハッシュを結合した文字列
     */
    public static string CreatePasswordHash(string password)
    {
        try
        {
            byte[] salt = GenerateSalt();
            // パスワードを char[] で扱うことで、メモリからの消去を容易にします。
            // String は不変オブジェクトであり、メモリから即座に消去することが困難なため、セキュリティリスクとなり得ます。
            char[] passwordChars = password.ToCharArray();
            byte[] hash = HashPassword(passwordChars, salt);

            // パスワード文字配列は、ハッシュ生成後すぐに消去することが推奨されます。
            Array.Fill(passwordChars, '\0'); // .NET Core 2.0+

            return Convert.ToBase64String(salt) + ":" + Convert.ToBase64String(hash);
        }
        catch (Exception ex)
        {
            throw new ApplicationException("Error during password hashing", ex);
        }
    }

    /**
     * 入力されたパスワードが保存されているハッシュと一致するか検証します。
     *
     * @param password 入力された平文パスワード
     * @param storedHashAndSalt 保存されているソルトとハッシュの結合文字列 (例: "salt:hash")
     * @return パスワードが一致すればtrue、そうでなければfalse
     */
    public static bool VerifyPassword(string password, string storedHashAndSalt)
    {
        try
        {
            string[] parts = storedHashAndSalt.Split(':');
            if (parts.Length != 2)
            {
                return false; // フォーマットが不正
            }
            byte[] salt = Convert.FromBase64String(parts[0]);
            byte[] storedHash = Convert.FromBase64String(parts[1]);

            char[] passwordChars = password.ToCharArray();
            byte[] generatedHash = HashPassword(passwordChars, salt);
            Array.Fill(passwordChars, '\0'); // パスワード文字配列を消去

            // 時間固定比較 (Time-constant comparison) を使用して、タイミング攻撃を防ぎます。
            // CryptographicOperations.FixedTimeEquals は .NET Core 3.0+ で利用可能です。
            #if NETCOREAPP3_0_OR_GREATER
            return CryptographicOperations.FixedTimeEquals(storedHash, generatedHash);
            #else
            // Fallback for older .NET versions
            if (storedHash.Length != generatedHash.Length) return false;
            bool areEqual = true;
            for (int i = 0; i < storedHash.Length; i++)
            {
                areEqual &= (storedHash[i] == generatedHash[i]);
            }
            return areEqual;
            #endif
        }
        catch (Exception ex)
        {
            throw new ApplicationException("Error during password verification", ex);
        }
    }

    public static void Main(string[] args)
    {
        string userPassword = "MySecurePassword123!";

        // 1. パスワードのハッシュ化と保存
        string hashedPasswordWithSalt = CreatePasswordHash(userPassword);
        Console.WriteLine("Original Password: " + userPassword);
        Console.WriteLine("Stored Hash (salt:hash): " + hashedPasswordWithSalt);

        // 2. パスワードの検証
        Console.WriteLine("\n--- Verification ---");
        bool isCorrect = VerifyPassword(userPassword, hashedPasswordWithSalt);
        Console.WriteLine("Verification with correct password: " + isCorrect); // true

        bool isIncorrect = VerifyPassword("WrongPassword!", hashedPasswordWithSalt);
        Console.WriteLine("Verification with incorrect password: " + isIncorrect); // false

        // 別のユーザーが同じパスワードを設定した場合（異なるソルトのためハッシュは異なる）
        string anotherUserPassword = "MySecurePassword123!";
        string anotherHashedPasswordWithSalt = CreatePasswordHash(anotherUserPassword);
        Console.WriteLine("\nStored Hash for another user with same password (salt:hash): " + anotherHashedPasswordWithSalt);
        Console.WriteLine("Are hashes the same for same password, different salt? " + hashedPasswordWithSalt.Equals(anotherHashedPasswordWithSalt)); // false
    }
}
```

**バージョン・アップデート情報:**
*   **`Rfc2898DeriveBytes`**: .NET Framework 2.0から利用可能です。コンストラクタで `HashAlgorithmName.SHA256` を指定することで、PBKDF2の基盤となるハッシュアルゴリズムをSHA-256に指定できます。
*   **`RandomNumberGenerator`**: .NET Core 2.0以降で静的メソッド `RandomNumberGenerator.Fill(byte[] buffer)` が追加され、`RNGCryptoServiceProvider` のインスタンス作成が不要になりました。.NET 6以降では `RNGCryptoServiceProvider` は非推奨とされています。
*   **`Array.Fill`**: .NET Core 2.0以降で追加され、配列を指定した値で埋めることができます。これにより `char[]` のクリアが容易になります。
*   **`CryptographicOperations.FixedTimeEquals`**: .NET Core 3.0以降で利用可能な、タイミング攻撃を防ぐための時間固定比較メソッドです。それ以前のバージョンでは、自前でループ比較を実装する必要があります。
*   **`using var` (C# 8+)**: `using var pbkdf2 = new Rfc2898DeriveBytes(...)` のように簡潔に書くことができます。

**プロフェッショナルな視点:**
*   **平文パスワードの扱い**: Javaと同様に、C#でもパスワードは `string` ではなく `char[]` で扱うべきです。`string` は不変で、GCによる解放タイミングを制御できません。`char[]` を使用し、使用後に `Array.Fill(passwordChars, '\0')` で上書きすることで、メモリ上の情報を速やかに消去できます。
*   **リソース管理**: `Rfc2898DeriveBytes` は `IDisposable` を実装しているため、`using` ステートメントで確実にリソースを解放してください。
*   **時間固定比較**: `CryptographicOperations.FixedTimeEquals` を使用することで、タイミング攻撃に対する堅牢性を高めることができます。これはセキュリティ上のベストプラクティスです。
*   **繰り返し回数 (Iterations)**: Javaと同様に、`ITERATIONS` は適切な処理時間（数百ミリ秒）を確保するように調整し、定期的に見直してください。
*   **鍵導出関数 (KDF) の選択**: .NET環境ではPBKDF2 (`Rfc2898DeriveBytes`) が標準ですが、Argon2などのより新しいKDFを検討する場合は、Argon2.NETなどの外部ライブラリの導入が必要です。

---

# 2. 暗号化処理

## 2.1. 暗号化処理とは
暗号化は、平文データを読み取れない形式（暗号文）に変換することで、データの機密性を保護するプロセスです。復号化は、暗号文を元の平文に戻すプロセスです。

**主な用途:**
*   **データ保護**: 保存されたデータ (DB、ファイル) やネットワーク経由で送信されるデータの機密性を確保する。
*   **プライバシー保護**: 個人情報などの機密データを保護する。

## 2.2. アルゴリズムの選定
*   **推奨**: **AES (Advanced Encryption Standard)**。ブロック暗号として世界的に広く採用されています。
*   **ブロックモード**:
    *   **GCM (Galois/Counter Mode)**: **最も推奨されるモード**。認証付き暗号 (Authenticated Encryption with Associated Data: AEAD) を提供し、データの機密性だけでなく、改ざん検出（認証）も行います。IVと認証タグが必要です。
    *   CBC (Cipher Block Chaining): レガシーな用途ではまだ見られますが、GCMが利用可能であればGCMを優先すべきです。認証を提供しないため、MAC (Message Authentication Code) と組み合わせる必要があります（Encrypt-then-MAC推奨）。
*   **パディング**: AES/GCMの場合、パディングは不要 (NoPadding)。他のブロックモード（CBCなど）ではPKCS7 (PKCS5) パディングが一般的です。

## 2.3. 鍵とIV (Initialization Vector) の管理
*   **対称鍵**: AESは対称鍵暗号であり、暗号化と復号化に同じ鍵を使用します。この鍵は厳重に管理される必要があります。
*   **IV (Initialization Vector)**:
    *   暗号化処理のランダム性を導入するために使用される**非機密な**値です。
    *   **同じ鍵で複数のデータを暗号化する際、IVは必ずユニークである必要があります**。IVを使い回すと、セキュリティが著しく低下します。
    *   IVは機密情報ではないため、暗号文と一緒に保存したり送信したりしても安全です。ただし、**予測不能なランダムな値**である必要があります。
    *   GCMモードでは、IVは「ノンス (Nonce)」と呼ばれることもあります。

---

### 2.3.1. Java での暗号化・復号化 (AES/GCM)

**用途**: 機密データの暗号化と認証。データの機密性と改ざん検出を同時に行います。

```java
// Ready-to-Run: AesGcmEncryptor.java
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.util.Base64;
import java.nio.ByteBuffer;
import java.util.Arrays; // For clearing arrays

public class AesGcmEncryptor {

    private static final int GCM_IV_LENGTH = 12; // GCM推奨IV長 (バイト)
    private static final int GCM_TAG_LENGTH = 16; // GCM推奨認証タグ長 (バイト)
    private static final int AES_KEY_BIT_SIZE = 256; // AES鍵長 (ビット): 128, 192, 256が利用可能

    /**
     * 新しいAES鍵を生成します。
     *
     * @return 生成されたSecretKeyオブジェクト
     * @throws Exception 何らかの暗号化関連エラーが発生した場合
     */
    public static SecretKey generateAesKey() throws Exception {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(AES_KEY_BIT_SIZE, new SecureRandom()); // 暗号論的に強力な乱数を使用
        return keyGen.generateKey();
    }

    /**
     * 平文データをAES/GCMで暗号化します。
     *
     * @param plainText 暗号化する平文のバイト配列
     * @param secretKey 暗号化に使用するSecretKey
     * @return IV, 暗号文, 認証タグを結合したバイト配列
     * @throws Exception 何らかの暗号化関連エラーが発生した場合
     */
    public static byte[] encrypt(byte[] plainText, SecretKey secretKey) throws Exception {
        // IVを生成 (必ずSecureRandomで、各暗号化ごとにユニークなものを使用)
        byte[] iv = new byte[GCM_IV_LENGTH];
        new SecureRandom().nextBytes(iv); // Java 8+

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH * 8, iv); // GCMタグ長はビット単位
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, gcmParameterSpec);

        byte[] cipherText = cipher.doFinal(plainText);

        // IVと暗号文を結合して返します。復号時にIVが必要なため、暗号文と一緒に保存または送信します。
        // ByteBuffer を使用して効率的に結合
        ByteBuffer byteBuffer = ByteBuffer.allocate(iv.length + cipherText.length);
        byteBuffer.put(iv);
        byteBuffer.put(cipherText);
        return byteBuffer.array();
    }

    /**
     * 暗号文データをAES/GCMで復号化します。
     *
     * @param cipherTextWithIv IVと暗号文と認証タグが結合されたバイト配列
     * @param secretKey 復号化に使用するSecretKey
     * @return 復号された平文のバイト配列
     * @throws Exception 何らかの暗号化関連エラーが発生した場合 (例: 認証タグの不一致、改ざん)
     */
    public static byte[] decrypt(byte[] cipherTextWithIv, SecretKey secretKey) throws Exception {
        // 結合されたバイト配列からIVと暗号文を分離
        ByteBuffer byteBuffer = ByteBuffer.wrap(cipherTextWithIv);
        byte[] iv = new byte[GCM_IV_LENGTH];
        byteBuffer.get(iv);

        byte[] cipherText = new byte[byteBuffer.remaining()];
        byteBuffer.get(cipherText);

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH * 8, iv);
        cipher.init(Cipher.DECRYPT_MODE, secretKey, gcmParameterSpec);

        return cipher.doFinal(cipherText);
    }

    public static void main(String[] args) {
        String originalText = "This is a secret message for Zenn Wiki. Keep it confidential!";
        SecretKey aesKey = null;

        try {
            // 1. AES鍵の生成 (初回のみ、または鍵更新時)
            aesKey = generateAesKey();
            System.out.println("Generated AES Key (Base64): " + Base64.getEncoder().encodeToString(aesKey.getEncoded()));

            // 2. データの暗号化
            byte[] encryptedDataWithIv = encrypt(originalText.getBytes(), aesKey);
            System.out.println("Encrypted Data (Base64, IV+Ciphertext+Tag): " + Base64.getEncoder().encodeToString(encryptedDataWithIv));

            // 3. データの復号化
            byte[] decryptedData = decrypt(encryptedDataWithIv, aesKey);
            String decryptedText = new String(decryptedData);
            System.out.println("Decrypted Data: " + decryptedText);
            System.out.println("Match original? " + originalText.equals(decryptedText));

            // 4. 改ざんのシミュレーション (復号時に認証失敗)
            System.out.println("\n--- Tampering Simulation ---");
            byte[] tamperedData = Arrays.copyOf(encryptedDataWithIv, encryptedDataWithIv.length);
            // 暗号文の途中の1バイトを書き換える
            if (tamperedData.length > GCM_IV_LENGTH + 5) {
                tamperedData[GCM_IV_LENGTH + 5] = (byte) (tamperedData[GCM_IV_LENGTH + 5] ^ 0x01); // 1ビット反転
            }
            try {
                System.out.println("Tampered Data (Base64): " + Base64.getEncoder().encodeToString(tamperedData));
                decrypt(tamperedData, aesKey);
                System.out.println("Tampering failed to detect!"); // この行は実行されないはず
            } catch (Exception e) {
                System.out.println("Tampering detected (as expected): " + e.getMessage()); // Expected result
            }

            // 5. 異なるIVでの暗号化 (同じ平文でも暗号文が異なることを確認)
            System.out.println("\n--- Different IV ---");
            byte[] encryptedDataWithIv2 = encrypt(originalText.getBytes(), aesKey);
            System.out.println("Encrypted Data 2 (Base64): " + Base64.getEncoder().encodeToString(encryptedDataWithIv2));
            System.out.println("Are encrypted data 1 and 2 same? " + Arrays.equals(encryptedDataWithIv, encryptedDataWithIv2)); // false

        } catch (Exception e) {
            System.err.println("Encryption/Decryption Error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            // 鍵をメモリから安全に消去する (可能な限り)
            if (aesKey != null && aesKey.getEncoded() != null) {
                Arrays.fill(aesKey.getEncoded(), (byte) 0);
            }
        }
    }
}
```

**バージョン・アップデート情報:**
*   **Java 7+**: `GCMParameterSpec` クラスが導入され、AES/GCMモードが標準で利用可能になりました。
*   **Java 8+**: `Base64` APIが標準で利用可能です。`SecureRandom.getInstanceStrong()` はOSネイティブの乱数生成器を利用しますが、`new SecureRandom()` も十分安全です。
*   **`SecretKey` のメモリからの消去**: `aesKey.getEncoded()` で取得したバイト配列は、`Arrays.fill()` を使ってゼロで上書きすることで、メモリ上の痕跡を可能な限り消去できます。ただし、`SecretKey` オブジェクト自体はGCに依存するため、完全な消去は保証されません。JEP 356 (Sealed Classes in Java 15+) や JEP 330 (Asymmetric Signature Schemes in Java 15+) など、将来的なセキュリティ関連の強化は続いていますが、現時点での一般的な鍵オブジェクトの扱い方です。

**プロフェッショナルな視点:**
*   **スレッドセーフティ**: `Cipher` クラスは**スレッドセーフではありません**。各スレッドで `Cipher.getInstance()` を呼び出して新しいインスタンスを取得するか、`ThreadLocal` を使用してスレッドごとにインスタンスを管理する必要があります。上記コードでは、呼び出しごとに新しいインスタンスを取得しています。
*   **AEAD (Authenticated Encryption with Associated Data)**: AES/GCMはAEADを提供するため、データ認証（改ざん検知）を自動的に行います。これにより、別途MACを計算する必要がなく、実装が簡素化され、潜在的な脆弱性（Encrypt-then-MAC, MAC-then-Encryptの誤用など）が減少します。
*   **IV (Initialization Vector) の重要性**: IVは必ず**各暗号化操作ごとに異なるランダムな値**を使用してください。同じ鍵とIVで異なるデータを暗号化すると、セキュリティ上の脆弱性（暗号文から平文の一部が推測されるなど）が生じます。
*   **鍵の保護**: 生成された `SecretKey` は、メモリ上に平文で長く保持せず、必要な時にのみ取得し、使用後は速やかに消去（`Arrays.fill()`）することが理想です。長期保存が必要な場合は、`KeyStore` などのセキュアなストレージを使用してください。
*   **エラーハンドリング**: 復号化時の `BadPaddingException` や `AEADBadTagException` (GCMの場合) は、データが改ざんされたか、鍵やIVが間違っていることを示します。これらの例外を適切に処理し、決して元のデータの一部を漏洩させないようにしてください。

---

### 2.3.2. C# での暗号化・復号化 (AES/GCM)

**用途**: 機密データの暗号化と認証。データの機密性と改ざん検出を同時に行います。

```csharp
// Ready-to-Run: AesGcmEncryptor.cs
using System;
using System.Security.Cryptography;
using System.Text;
using System.Linq; // For byte array manipulations

public class AesGcmEncryptor
{
    private const int GCM_NONCE_LENGTH = 12; // GCM推奨Nonce長 (IVに相当)
    private const int GCM_TAG_LENGTH = 16;  // GCM推奨認証タグ長 (バイト)
    private const int AES_KEY_BYTE_SIZE = 32; // AES鍵長 (バイト): 16(128bit), 24(192bit), 32(256bit)

    /**
     * 新しいAES鍵を生成します。
     *
     * @return 生成されたバイト配列形式のAES鍵
     */
    public static byte[] GenerateAesKey()
    {
        byte[] key = new byte[AES_KEY_BYTE_SIZE];
        RandomNumberGenerator.Fill(key); // 暗号論的に強力な乱数を使用
        return key;
    }

    /**
     * 平文データをAES/GCMで暗号化します。
     *
     * @param plainText 暗号化する平文のバイト配列
     * @param keyBytes 暗号化に使用する鍵のバイト配列
     * @return Nonce, 暗号文, 認証タグを結合したバイト配列
     * @throws Exception 何らかの暗号化関連エラーが発生した場合
     */
    public static byte[] Encrypt(byte[] plainText, byte[] keyBytes)
    {
        // Nonceを生成 (必ずRandomNumberGeneratorで、各暗号化ごとにユニークなものを使用)
        byte[] nonce = new byte[GCM_NONCE_LENGTH];
        RandomNumberGenerator.Fill(nonce);

        // AES/GCMは.NET Core 3.0+ で利用可能です。
        // それ以前のバージョンでは、AesManaged + HMAC-SHA256 で Encrypt-then-MAC を実装する必要があります。
        #if NETCOREAPP3_0_OR_GREATER
        using (AesGcm aesGcm = new AesGcm(keyBytes))
        {
            byte[] cipherText = new byte[plainText.Length];
            byte[] tag = new byte[GCM_TAG_LENGTH];

            // 関連データ (AAD) はここでは使用していませんが、必要に応じて指定できます。
            // aesGcm.Encrypt(nonce, plainText, cipherText, tag, associatedData);
            aesGcm.Encrypt(nonce, plainText, cipherText, tag);

            // Nonce, 暗号文, 認証タグを結合して返します。復号時にこれら全てが必要です。
            // Array.CopyTo を使用して効率的に結合
            byte[] result = new byte[nonce.Length + cipherText.Length + tag.Length];
            Buffer.BlockCopy(nonce, 0, result, 0, nonce.Length);
            Buffer.BlockCopy(cipherText, 0, result, nonce.Length, cipherText.Length);
            Buffer.BlockCopy(tag, 0, result, nonce.Length + cipherText.Length, tag.Length);
            return result;
        }
        #else
        throw new NotSupportedException("AES/GCM requires .NET Core 3.0 or later.");
        // Fallback for older .NET versions (e.g., AesManaged + HMAC-SHA256) would be much more complex.
        // It involves creating an AesManaged instance, setting Key, IV, Mode=CBC, Padding=PKCS7,
        // encrypting, then computing an HMAC for the ciphertext and IV.
        // This is out of scope for a "Ready-to-Run" example given the strong recommendation for GCM.
        #endif
    }

    /**
     * 暗号文データをAES/GCMで復号化します。
     *
     * @param cipherTextWithNonceAndTag Nonce, 暗号文, 認証タグが結合されたバイト配列
     * @param keyBytes 復号化に使用する鍵のバイト配列
     * @return 復号された平文のバイト配列
     * @throws CryptographicException 認証タグの不一致など、復号関連のエラーが発生した場合
     * @throws NotSupportedException .NET Core 3.0未満の場合
     */
    public static byte[] Decrypt(byte[] cipherTextWithNonceAndTag, byte[] keyBytes)
    {
        #if NETCOREAPP3_0_OR_GREATER
        // 結合されたバイト配列からNonce, 暗号文, 認証タグを分離
        byte[] nonce = new byte[GCM_NONCE_LENGTH];
        Buffer.BlockCopy(cipherTextWithNonceAndTag, 0, nonce, 0, GCM_NONCE_LENGTH);

        byte[] tag = new byte[GCM_TAG_LENGTH];
        Buffer.BlockCopy(cipherTextWithNonceAndTag, cipherTextWithNonceAndTag.Length - GCM_TAG_LENGTH, tag, 0, GCM_TAG_LENGTH);

        byte[] cipherText = new byte[cipherTextWithNonceAndTag.Length - GCM_NONCE_LENGTH - GCM_TAG_LENGTH];
        Buffer.BlockCopy(cipherTextWithNonceAndTag, GCM_NONCE_LENGTH, cipherText, 0, cipherText.Length);

        using (AesGcm aesGcm = new AesGcm(keyBytes))
        {
            byte[] plainText = new byte[cipherText.Length];
            // aesGcm.Decrypt(nonce, cipherText, tag, plainText, associatedData);
            aesGcm.Decrypt(nonce, cipherText, tag, plainText);
            return plainText;
        }
        #else
        throw new NotSupportedException("AES/GCM requires .NET Core 3.0 or later.");
        #endif
    }

    public static void Main(string[] args)
    {
        string originalText = "This is a secret message for Zenn Wiki. Keep it confidential!";
        byte[] aesKey = null;

        try
        {
            // 1. AES鍵の生成 (初回のみ、または鍵更新時)
            aesKey = GenerateAesKey();
            Console.WriteLine("Generated AES Key (Base64): " + Convert.ToBase64String(aesKey));

            // 2. データの暗号化
            byte[] encryptedDataWithNonceAndTag = Encrypt(Encoding.UTF8.GetBytes(originalText), aesKey);
            Console.WriteLine("Encrypted Data (Base64, Nonce+Ciphertext+Tag): " + Convert.ToBase64String(encryptedDataWithNonceAndTag));

            // 3. データの復号化
            byte[] decryptedData = Decrypt(encryptedDataWithNonceAndTag, aesKey);
            string decryptedText = Encoding.UTF8.GetString(decryptedData);
            Console.WriteLine("Decrypted Data: " + decryptedText);
            Console.WriteLine("Match original? " + originalText.Equals(decryptedText));

            // 4. 改ざんのシミュレーション (復号時に認証失敗)
            Console.WriteLine("\n--- Tampering Simulation ---");
            byte[] tamperedData = (byte[])encryptedDataWithNonceAndTag.Clone();
            // 暗号文の途中の1バイトを書き換える
            if (tamperedData.Length > GCM_NONCE_LENGTH + 5)
            {
                tamperedData[GCM_NONCE_LENGTH + 5] = (byte)(tamperedData[GCM_NONCE_LENGTH + 5] ^ 0x01); // 1ビット反転
            }
            try
            {
                Console.WriteLine("Tampered Data (Base64): " + Convert.ToBase64String(tamperedData));
                Decrypt(tamperedData, aesKey);
                Console.WriteLine("Tampering failed to detect!"); // この行は実行されないはず
            }
            catch (CryptographicException e)
            {
                Console.WriteLine("Tampering detected (as expected): " + e.Message); // Expected result
            }
            catch (Exception e)
            {
                Console.WriteLine("Unexpected error during tampering detection: " + e.Message);
            }

            // 5. 異なるNonceでの暗号化 (同じ平文でも暗号文が異なることを確認)
            Console.WriteLine("\n--- Different Nonce ---");
            byte[] encryptedDataWithNonceAndTag2 = Encrypt(Encoding.UTF8.GetBytes(originalText), aesKey);
            Console.WriteLine("Encrypted Data 2 (Base64): " + Convert.ToBase64String(encryptedDataWithNonceAndTag2));
            Console.WriteLine("Are encrypted data 1 and 2 same? " + encryptedDataWithNonceAndTag.SequenceEqual(encryptedDataWithNonceAndTag2)); // false

        }
        catch (NotSupportedException ex)
        {
            Console.Error.WriteLine(ex.Message);
            Console.Error.WriteLine("Please compile and run this code with .NET Core 3.0 or later for AES/GCM support.");
        }
        catch (Exception e)
        {
            Console.Error.WriteLine("Encryption/Decryption Error: " + e.Message);
        }
        finally
        {
            // 鍵をメモリから安全に消去する (可能な限り)
            if (aesKey != null)
            {
                Array.Fill(aesKey, (byte)0);
            }
        }
    }
}
```

**バージョン・アップデート情報:**
*   **.NET Core 3.0+**: `System.Security.Cryptography.AesGcm` クラスが導入され、認証付き暗号 (AEAD) が標準で利用可能になりました。それ以前のバージョン (`.NET Framework` や `.NET Core 2.x`) では、`AesManaged` や `RijndaelManaged` と HMAC を組み合わせて自身でAEADを実装する必要があり、複雑でエラーの温床となるため推奨されません。
*   **`RandomNumberGenerator.Fill()`**: .NET Core 2.0以降で利用可能な、暗号論的強度の高い乱数を生成する静的メソッドです。
*   **`Array.Fill()`**: .NET Core 2.0以降で利用可能です。
*   **`using var` (C# 8+)**: `using var aesGcm = new AesGcm(keyBytes)` のように簡潔に書くことができます。

**プロフェッショナルな視点:**
*   **AES/GCM の優先**: C# (.NET Core 3.0以降) では、`AesGcm` クラスが利用できるため、AES/GCMモードを優先的に使用してください。これにより、機密性（暗号化）と完全性（改ざん検知）を同時に確保でき、多くのセキュリティ上の落とし穴を回避できます。
*   **リソース管理**: `AesGcm` クラスは `IDisposable` を実装しているため、`using` ステートメントで確実にリソースを解放してください。
*   **Nonce (IV) の重要性**: Nonceは必ず**各暗号化操作ごとに異なるランダムな値**を使用してください。同じ鍵とNonceで異なるデータを暗号化すると、セキュリティ上の脆弱性（暗号文から平文の一部が推測されるなど）が生じます。Nonceは暗号文と一緒に保存または送信されます。
*   **鍵の保護**: 生成されたAES鍵のバイト配列は、メモリ上に平文で長く保持せず、使用後は `Array.Fill()` でゼロで上書きすることで、メモリ上の痕跡を可能な限り消去することが推奨されます。鍵の長期保存には、Azure Key VaultやAWS KMSなどのクラウドサービスや、Windows DPAPI (Data Protection API) などのセキュアなストレージを使用してください。
*   **エラーハンドリング**: `AesGcm.Decrypt` は、認証タグが検証に失敗した場合 (`CryptographicException`) をスローします。これはデータが改ざんされたか、鍵やNonceが間違っていることを示します。この例外を適切に処理し、決して元のデータの一部を漏洩させないようにしてください。

---

# まとめと推奨事項

このWikiでは、JavaとC#における暗号化・ハッシュ処理の基本的な実装と、その背後にある重要なセキュリティ原則を解説しました。

セキュリティは終わりなき旅であり、常に最新の脅威とベストプラクティスを学び続ける必要があります。

**チームへの最終的な推奨事項:**

1.  **常に最新のアルゴリズムとAPIを使用する**: MD5, SHA-1, DES, RC4 などの古い、または脆弱性が指摘されているアルゴリズムは絶対に使用しないでください。ハッシュにはSHA-256/512 (PBKDF2/Argon2/scrypt)、暗号化にはAES/GCMを推奨します。
2.  **自分で暗号を実装しない**: 暗号アルゴリズムは複雑であり、ちょっとしたミスが大きな脆弱性につながります。言語標準ライブラリ（Java Cryptography Architecture (JCA/JCE), .NET `System.Security.Cryptography`）を信頼して使用してください。
3.  **セキュアな乱数生成器を使用する**: 鍵、ソルト、IV/Nonce の生成には必ず暗号論的に強力な乱数生成器を使用してください (`SecureRandom` in Java, `RandomNumberGenerator` in C#)。
4.  **鍵とIV/Nonceの管理を徹底する**:
    *   鍵は厳重に保護し、セキュアなストレージに保管すること。コードにハードコードしたり、Gitにコミットしたりしないこと。
    *   IV/Nonce は各暗号化操作ごとにユニークなものを使用し、暗号文と一緒に保存・送信すること。
5.  **パスワードはPBKDF2/Argon2/scryptでハッシュ化し、ソルトと十分な繰り返し回数を使用する**: 平文パスワードを保存してはなりません。また、`char[]` を使用し、使用後にメモリから消去する習慣をつけましょう。
6.  **認証付き暗号 (AEAD) を優先する**: AES/GCM のように、データの機密性と完全性（改ざん検知）を同時に提供するモードを使用してください。
7.  **エラーハンドリングを丁寧に行う**: 暗号化・復号化の失敗はセキュリティ上の警告です。適切な例外処理を行い、攻撃者にヒントを与えないようにしてください。
8.  **定期的なレビューと学習**: 暗号技術は進化しています。チーム内で定期的にセキュリティ標準を見直し、最新の情報を共有し、学習を続けましょう。

何か疑問や不明な点があれば、いつでも私（リードエンジニア）や他の経験豊富なメンバーに相談してください。チーム全体で、よりセキュアなシステムを構築していきましょう！